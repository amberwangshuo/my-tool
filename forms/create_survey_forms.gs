/**
 * Génère le questionnaire « Le travail, la vie personnelle et vous »
 * dans Google Forms, à partir de Questionnaire_bilingue_v1.
 *
 * 使用方法 / Utilisation :
 *   1. Ouvrir https://script.google.com → « Nouveau projet »
 *   2. Coller tout ce fichier dans l'éditeur (remplacer le contenu existant)
 *   3. Choisir la fonction createFrenchForm (ou createChineseForm) puis « Exécuter »
 *   4. Autoriser l'accès quand Google le demande
 *   5. Les URL (édition + diffusion) s'affichent dans le journal d'exécution
 *
 * Les deux versions gardent la même numérotation (A0…E12) afin que les
 * données des deux plateformes puissent être fusionnées.
 */

// ---------------------------------------------------------------------------
// Points d'entrée
// ---------------------------------------------------------------------------

function createFrenchForm() {
  buildForm(FR);
}

function createChineseForm() {
  buildForm(ZH);
}

// ---------------------------------------------------------------------------
// Construction du formulaire (structure commune aux deux langues)
// ---------------------------------------------------------------------------

function buildForm(L) {
  var form = FormApp.create(L.fileName);

  form.setTitle(L.title)
      .setDescription(L.intro)
      .setProgressBar(true)
      .setAllowResponseEdits(false)
      .setShowLinkToRespondAgain(false)
      .setConfirmationMessage(L.confirmation);

  // Anonymat : aucune adresse e-mail collectée. Google a introduit
  // setEmailCollectionType() en remplacement de setCollectEmail() ; on essaie
  // la nouvelle API puis on retombe sur l'ancienne selon la version du runtime.
  try {
    form.setEmailCollectionType(FormApp.EmailCollectionType.DO_NOT_COLLECT);
  } catch (e) {
    form.setCollectEmail(false);
  }

  // --- Page 1 : consentement + filtre d'éligibilité --------------------------
  form.addCheckboxItem()
      .setTitle(L.consent)
      .setChoiceValues([L.consentYes])
      .setRequired(true);

  var a0 = form.addMultipleChoiceItem().setTitle("A0. " + L.a0).setRequired(true);

  // --- Page 2 : section A, question filtre A1 -------------------------------
  var pageA = form.addPageBreakItem().setTitle(L.sectionA);
  var a1 = form.addMultipleChoiceItem().setTitle("A1. " + L.a1).setRequired(true);

  // --- Page 3 : détail du télétravail (seulement si A1 = oui) ---------------
  var pageTeleworkDetail = form.addPageBreakItem().setTitle(L.sectionATelework);
  addChoice(form, "A2. " + L.a2, L.a2Choices);
  addChoice(form, "A3. " + L.a3, L.a3Choices);
  addChoice(form, "A4. " + L.a4, L.a4Choices);
  addChoice(form, L.a4bisLabel + " " + L.a4bis, L.a4bisChoices);

  // --- Page 4 : parcours antérieur, question filtre A5 ----------------------
  var pageA5 = form.addPageBreakItem().setTitle(L.sectionAHistory);
  var a5 = form.addMultipleChoiceItem().setTitle("A5. " + L.a5).setRequired(true);

  // --- Page 5 : durée de l'expérience antérieure (seulement si A5 = oui) ----
  var pageA6 = form.addPageBreakItem().setTitle(L.sectionAHistory);
  addChoice(form, "A6. " + L.a6, L.a6Choices);

  // --- Page 6 : stabilité du mode de travail actuel -------------------------
  var pageA7 = form.addPageBreakItem().setTitle(L.sectionAHistory);
  addChoice(form, "A7. " + L.a7, L.a7Choices);

  // --- Page 7 : section B (Hayman, 16 énoncés dont 1 test d'attention) ------
  form.addPageBreakItem().setTitle(L.sectionB).setHelpText(L.sectionBHelp);
  form.addGridItem()
      .setTitle(L.gridTitleB)
      .setRows(L.bItems)
      .setColumns(L.agreementScale)
      .setRequired(true);

  // --- Page 8 : section C (IWPQ, 13 énoncés) --------------------------------
  form.addPageBreakItem().setTitle(L.sectionC).setHelpText(L.sectionCHelp);
  form.addGridItem()
      .setTitle(L.gridTitleC)
      .setRows(L.cItems)
      .setColumns(L.frequencyScale)
      .setRequired(true);

  // --- Page 9 : section D (QVCT, 0-10) --------------------------------------
  form.addPageBreakItem().setTitle(L.sectionD);
  form.addScaleItem()
      .setTitle("D1. " + L.d1)
      .setBounds(0, 10)
      .setLabels(L.d1Low, L.d1High)
      .setRequired(true);

  // --- Page 10 : section E (caractéristiques personnelles) ------------------
  var pageE = form.addPageBreakItem().setTitle(L.sectionE);
  addChoice(form, "E1. " + L.e1, L.e1Choices);
  addChoice(form, "E2. " + L.e2, L.e2Choices);
  addChoice(form, "E3. " + L.e3, L.e3Choices);
  addChoice(form, "E4. " + L.e4, L.e4Choices);
  addChoice(form, "E5. " + L.e5, L.e5Choices);
  addChoice(form, "E6. " + L.e6, L.e6Choices);
  addChoice(form, "E7. " + L.e7, L.e7Choices);
  addChoice(form, "E8. " + L.e8, L.e8Choices);
  addChoice(form, "E9. " + L.e9, L.e9Choices);
  addChoice(form, "E10. " + L.e10, L.e10Choices);
  addChoice(form, "E11. " + L.e11, L.e11Choices);
  addChoice(form, "E12. " + L.e12, L.e12Choices);

  // --- Page 11 : sortie anticipée pour les non-salariés ---------------------
  var pageIneligible = form.addPageBreakItem()
      .setTitle(L.ineligibleTitle)
      .setHelpText(L.ineligibleText);

  // --- Logique de navigation ------------------------------------------------
  // Les sauts sont posés en dernier : les PageBreakItem cibles doivent exister.

  // A0 : non salarié → page de remerciement anticipé
  a0.setChoices([
    a0.createChoice(L.yes, pageA),
    a0.createChoice(L.no, pageIneligible)
  ]);

  // A1 : télétravaille → détail ; sinon → on saute directement à A5
  a1.setChoices([
    a1.createChoice(L.yes, pageTeleworkDetail),
    a1.createChoice(L.no, pageA5)
  ]);

  // A5 : a connu un autre mode de travail → A6 ; sinon → A7
  a5.setChoices([
    a5.createChoice(L.hasYes, pageA6),
    a5.createChoice(L.hasNo, pageA7)
  ]);

  // Fin du parcours normal : soumettre sans passer par la page « non éligible »
  pageE.setGoToPage(FormApp.PageNavigationType.SUBMIT);

  // Les pages intermédiaires enchaînent dans l'ordre naturel.
  pageTeleworkDetail.setGoToPage(pageA5);
  pageA6.setGoToPage(pageA7);

  Logger.log("Formulaire créé : " + L.fileName);
  Logger.log("URL d'édition   : " + form.getEditUrl());
  Logger.log("URL de diffusion : " + form.getPublishedUrl());
}

/** Ajoute une question à choix unique, obligatoire. */
function addChoice(form, title, choices) {
  return form.addMultipleChoiceItem()
             .setTitle(title)
             .setChoiceValues(choices)
             .setRequired(true);
}

// ---------------------------------------------------------------------------
// VERSION FRANÇAISE
// ---------------------------------------------------------------------------

var FR = {
  fileName: "Le travail, la vie personnelle et vous (FR)",
  title: "Le travail, la vie personnelle et vous",

  intro:
    "Cette enquête est réalisée dans le cadre d’un mémoire de Master 2 en gestion des ressources humaines. " +
    "Elle porte sur le télétravail, l’articulation entre vie professionnelle et vie personnelle et la manière " +
    "dont les salariés perçoivent leur travail. Elle s’adresse à toute personne actuellement en emploi salarié, " +
    "qu’elle pratique ou non le télétravail.\n\n" +
    "Le questionnaire comporte une cinquantaine de questions à choix unique et demande 7 à 9 minutes. " +
    "Les réponses sont strictement anonymes. Aucune donnée permettant de vous identifier n’est collectée. " +
    "Les réponses seront utilisées uniquement à des fins académiques et détruites à l’issue de la recherche. " +
    "Vous pouvez interrompre votre participation à tout moment.",

  consent: "Consentement",
  consentYes: "J’ai pris connaissance de ces informations et j’accepte de participer.",

  yes: "Oui",
  no: "Non",
  hasYes: "Oui",
  hasNo: "Non",

  a0: "Êtes-vous actuellement en emploi salarié ?",

  sectionA: "A. Votre situation professionnelle actuelle",
  sectionATelework: "A. Votre situation professionnelle actuelle",
  sectionAHistory: "A. Votre situation professionnelle actuelle",

  a1: "Actuellement, télétravaillez-vous au moins un jour par semaine ?",

  a2: "En moyenne, combien de jours par semaine télétravaillez-vous ?",
  a2Choices: ["Moins d’un jour", "1 jour", "2 jours", "3 jours", "4 jours", "5 jours ou plus"],

  a3: "Quelle part de votre temps de travail total le télétravail représente-t-il ?",
  a3Choices: ["Moins de 20 %", "20 à 40 %", "41 à 60 %", "61 à 80 %", "Plus de 80 %"],

  a4: "Depuis combien de temps télétravaillez-vous régulièrement ?",
  a4Choices: ["Moins de 3 mois", "3 à 12 mois", "1 à 3 ans", "Plus de 3 ans"],

  a4bisLabel: "A4 bis.",
  a4bis: "Dans votre cas, le télétravail relève principalement…",
  a4bisChoices: ["D’un choix personnel", "D’une décision de l’employeur", "Des deux"],

  a5: "Au cours de votre parcours professionnel, avez-vous déjà connu un mode de travail différent de votre " +
      "situation actuelle (du télétravail si vous n’en pratiquez pas aujourd’hui, un travail entièrement sur " +
      "site si vous télétravaillez) ?",

  a6: "Pendant combien de temps ?",
  a6Choices: ["Moins de 3 mois", "3 à 12 mois", "Plus d’un an"],

  a7: "Depuis combien de temps votre mode de travail actuel (télétravail ou travail sur site) est-il stable ?",
  a7Choices: ["Moins d’un mois", "1 à 3 mois", "Plus de 3 mois"],

  sectionB: "B. Votre vie professionnelle et votre vie personnelle",
  sectionBHelp:
    "Les affirmations suivantes portent sur les trois derniers mois. " +
    "Pour chacune, indiquez votre degré d’accord.",
  gridTitleB: "Indiquez votre degré d’accord avec chacune de ces affirmations.",

  agreementScale: [
    "1 Pas du tout d’accord",
    "2 Plutôt pas d’accord",
    "3 Ni d’accord ni pas d’accord",
    "4 Plutôt d’accord",
    "5 Tout à fait d’accord"
  ],

  bItems: [
    "B1. Ma vie personnelle souffre de mon travail.",
    "B2. Mon travail rend ma vie personnelle difficile.",
    "B3. Je néglige mes besoins personnels à cause de mon travail.",
    "B4. Je mets ma vie personnelle de côté pour mon travail.",
    "B5. Je manque des activités personnelles à cause de mon travail.",
    "B6. J’ai du mal à concilier mes activités professionnelles et personnelles.",
    "B7. Je suis insatisfait(e) du temps qu’il me reste pour ma vie personnelle.",
    "B8. Ma vie personnelle me prend de l’énergie dont j’aurais besoin pour mon travail.",
    "B9. Je suis trop fatigué(e) par ma vie personnelle pour être efficace au travail.",
    "B10. Mon travail souffre de ma vie personnelle.",
    "B11. J’ai du mal à travailler à cause de mes préoccupations personnelles.",
    "B12. Pour vérifier votre attention, veuillez sélectionner ici « Pas du tout d’accord ».",
    "B13. Ma vie personnelle me donne de l’énergie pour mon travail.",
    "B14. Mon travail me donne de l’énergie pour mes activités personnelles.",
    "B15. Je suis de meilleure humeur au travail grâce à ma vie personnelle.",
    "B16. Je suis de meilleure humeur dans ma vie personnelle grâce à mon travail."
  ],

  sectionC: "C. Votre travail au cours des trois derniers mois",
  sectionCHelp:
    "Les affirmations suivantes décrivent des comportements au travail. Pour chacune, indiquez la fréquence " +
    "qui correspond à votre situation au cours des trois derniers mois.",
  gridTitleC: "Indiquez la fréquence qui correspond à votre situation.",

  frequencyScale: ["1 Jamais", "2 Rarement", "3 Parfois", "4 Souvent", "5 Très souvent"],

  cItems: [
    "C1. J’ai réussi à planifier mon travail de manière à le terminer dans les délais.",
    "C2. Mon organisation du travail a été optimale.",
    "C3. J’ai gardé à l’esprit les résultats que je devais atteindre.",
    "C4. J’ai su distinguer l’essentiel de l’accessoire dans mon travail.",
    "C5. J’ai été capable de bien réaliser mon travail en y consacrant un minimum de temps et d’efforts.",
    "C6. J’ai assumé des responsabilités supplémentaires.",
    "C7. J’ai entrepris de nouvelles tâches de ma propre initiative, une fois les précédentes terminées.",
    "C8. J’ai accepté des tâches stimulantes lorsqu’elles se présentaient.",
    "C9. J’ai veillé à maintenir à jour mes connaissances professionnelles.",
    "C10. J’ai veillé à maintenir à jour mes compétences professionnelles.",
    "C11. J’ai proposé des solutions créatives à des problèmes nouveaux.",
    "C12. J’ai continué à rechercher de nouveaux défis dans mon travail.",
    "C13. J’ai participé activement aux réunions de travail."
  ],

  sectionD: "D. Votre organisation",
  d1: "De manière générale, comment évaluez-vous la qualité de vie et des conditions de travail au sein de " +
      "votre organisation ?",
  d1Low: "Très mauvaise",
  d1High: "Excellente",

  sectionE: "E. Pour mieux vous connaître",

  e1: "Dans quel pays exercez-vous principalement votre activité ?",
  e1Choices: ["France", "Chine", "Autre"],

  e2: "Vous êtes…",
  e2Choices: ["Une femme", "Un homme", "Autre / je préfère ne pas répondre"],

  e3: "Votre âge",
  e3Choices: ["Moins de 25 ans", "25 à 34 ans", "35 à 44 ans", "45 à 54 ans", "55 ans et plus"],

  e4: "Vivez-vous en couple ?",
  e4Choices: ["Oui", "Non"],

  e5: "Avez-vous des enfants à charge ?",
  e5Choices: ["Aucun", "Oui, dont au moins un de moins de 12 ans", "Oui, tous âgés de 12 ans ou plus"],

  e6: "Votre diplôme le plus élevé",
  e6Choices: ["Inférieur au baccalauréat", "Baccalauréat", "Bac +2 / +3", "Bac +4 / +5", "Supérieur à Bac +5"],

  e7: "Votre statut",
  e7Choices: ["Cadre ou équivalent", "Non cadre"],

  e8: "Le secteur de votre organisation",
  e8Choices: ["Industrie", "Commerce", "Services", "Administration publique", "Autre"],

  e9: "La taille de votre organisation",
  e9Choices: ["Moins de 50 salariés", "50 à 249", "250 à 999", "1 000 et plus"],

  e10: "Votre ancienneté dans votre organisation actuelle",
  e10Choices: ["Moins d’un an", "1 à 3 ans", "4 à 10 ans", "Plus de 10 ans"],

  e11: "Votre temps de trajet habituel entre votre domicile et votre lieu de travail (aller simple)",
  e11Choices: ["Moins de 15 minutes", "15 à 30 minutes", "31 à 45 minutes", "46 à 60 minutes", "Plus d’une heure"],

  e12: "Disposez-vous chez vous d’une pièce ou d’un espace dédié au travail ?",
  e12Choices: ["Oui", "Non"],

  ineligibleTitle: "Merci de votre intérêt",
  ineligibleText:
    "Ce questionnaire s’adresse uniquement aux personnes actuellement en emploi salarié. " +
    "Vous pouvez envoyer le formulaire ici : votre réponse ne sera pas retenue dans l’analyse. " +
    "Merci du temps que vous y avez consacré.",

  confirmation:
    "Merci de votre participation. Vos réponses contribuent à une recherche sur l’organisation du travail " +
    "menée auprès de salariés en France et en Chine."
};

// ---------------------------------------------------------------------------
// 中文版
// ---------------------------------------------------------------------------

var ZH = {
  fileName: "工作、生活与您（中文版）",
  title: "工作、生活与您",

  intro:
    "本问卷为一项人力资源管理硕士论文研究，主题是远程办公、工作与个人生活的兼顾，以及员工对自身工作表现的感知。" +
    "问卷面向所有目前在职的受雇人员，无论您是否远程办公均可填写。\n\n" +
    "问卷共约 50 道单选题，用时 7 至 9 分钟。所有回答完全匿名，不收集任何可识别您身份的信息。" +
    "数据仅用于学术研究，研究结束后即销毁。您可以随时中止填写。",

  consent: "知情同意",
  consentYes: "我已阅读上述说明，同意参与本调查。",

  yes: "是",
  no: "否",
  hasYes: "有",
  hasNo: "没有",

  a0: "您目前是否为在职受雇人员（有雇主的全职或兼职工作）？",

  sectionA: "A. 您目前的工作情况",
  sectionATelework: "A. 您目前的工作情况",
  sectionAHistory: "A. 您目前的工作情况",

  a1: "目前，您是否每周至少有一天远程办公（居家或在办公场所以外的地点工作）？",

  a2: "平均而言，您每周远程办公几天？",
  a2Choices: ["不足一天", "1 天", "2 天", "3 天", "4 天", "5 天及以上"],

  a3: "远程办公约占您全部工作时间的多大比例？",
  a3Choices: ["20% 以下", "20%–40%", "41%–60%", "61%–80%", "80% 以上"],

  a4: "您经常性远程办公有多长时间了？",
  a4Choices: ["不足 3 个月", "3 至 12 个月", "1 至 3 年", "3 年以上"],

  a4bisLabel: "A4 补.",
  a4bis: "就您的情况而言，远程办公主要是……",
  a4bisChoices: ["您个人的选择", "雇主的安排", "两者都有"],

  a5: "在您的职业经历中，是否曾有过与目前不同的工作方式（若您现在不远程办公，指曾经远程办公；" +
      "若您现在远程办公，指曾经完全在单位办公）？",

  a6: "那段经历持续了多久？",
  a6Choices: ["不足 3 个月", "3 至 12 个月", "1 年以上"],

  a7: "您目前的工作方式（远程或到岗）保持稳定有多久了？",
  a7Choices: ["不足 1 个月", "1 至 3 个月", "3 个月以上"],

  sectionB: "B. 您的工作与个人生活",
  sectionBHelp: "以下描述均针对最近三个月的情况。请就每一条表明您的同意程度。",
  gridTitleB: "请就以下每一条表明您的同意程度。",

  agreementScale: ["1 完全不同意", "2 比较不同意", "3 不确定", "4 比较同意", "5 完全同意"],

  bItems: [
    "B1. 我的个人生活因工作而受到影响。",
    "B2. 工作让我的个人生活变得困难。",
    "B3. 因为工作，我忽视了自己的个人需要。",
    "B4. 为了工作，我把个人生活搁置一旁。",
    "B5. 因为工作，我错过了不少个人活动。",
    "B6. 我很难兼顾工作和个人事务。",
    "B7. 我对留给个人生活的时间感到不满意。",
    "B8. 个人生活占用了我本应投入工作的精力。",
    "B9. 个人生活让我过于疲惫，影响了工作效率。",
    "B10. 我的工作因个人生活而受到影响。",
    "B11. 因为个人事务的困扰，我难以投入工作。",
    "B12. 为核实您是否认真作答，本题请选择“完全不同意”。",
    "B13. 个人生活为我的工作带来能量。",
    "B14. 工作让我更有精力去从事个人活动。",
    "B15. 因为个人生活顺心，我在工作中心情更好。",
    "B16. 因为工作顺利，我在个人生活中心情更好。"
  ],

  sectionC: "C. 最近三个月您的工作表现",
  sectionCHelp: "以下描述的是工作中的具体行为。请根据最近三个月的实际情况，选择相应的频率。",
  gridTitleC: "请根据最近三个月的实际情况选择频率。",

  frequencyScale: ["1 从不", "2 很少", "3 有时", "4 经常", "5 总是"],

  cItems: [
    "C1. 我能合理安排工作，按时完成任务。",
    "C2. 我对工作的安排是高效合理的。",
    "C3. 我在工作中始终记得自己要达成的目标。",
    "C4. 我能分清工作中的主次。",
    "C5. 我能用较少的时间和精力把工作做好。",
    "C6. 我承担了额外的工作职责。",
    "C7. 完成手头任务后，我会主动开始新的任务。",
    "C8. 有挑战性的任务出现时，我愿意接手。",
    "C9. 我注意及时更新自己的专业知识。",
    "C10. 我注意及时更新自己的专业技能。",
    "C11. 面对新问题，我能提出有创意的解决办法。",
    "C12. 我在工作中持续寻找新的挑战。",
    "C13. 我积极参与工作会议。"
  ],

  sectionD: "D. 您所在的组织",
  d1: "总体而言，您如何评价您所在组织的工作生活质量与工作条件？",
  d1Low: "非常差",
  d1High: "非常好",

  sectionE: "E. 关于您的基本情况",

  e1: "您主要在哪个国家工作？",
  e1Choices: ["法国", "中国", "其他"],

  e2: "您的性别",
  e2Choices: ["女", "男", "其他 / 不愿透露"],

  e3: "您的年龄",
  e3Choices: ["25 岁以下", "25–34 岁", "35–44 岁", "45–54 岁", "55 岁及以上"],

  e4: "您目前是否与伴侣共同生活？",
  e4Choices: ["是", "否"],

  e5: "您是否有需要抚养的子女？",
  e5Choices: ["没有", "有，其中至少一名未满 12 岁", "有，均已满 12 岁"],

  e6: "您的最高学历",
  e6Choices: ["高中及以下", "大专", "本科", "硕士", "博士"],

  e7: "您的岗位性质",
  e7Choices: ["管理岗位或同等职级", "非管理岗位"],

  e8: "您所在组织的行业",
  e8Choices: ["工业制造", "商贸", "服务业", "政府及公共机构", "其他"],

  e9: "您所在组织的规模",
  e9Choices: ["50 人以下", "50–249 人", "250–999 人", "1000 人及以上"],

  e10: "您在当前组织的工作年限",
  e10Choices: ["不足 1 年", "1–3 年", "4–10 年", "10 年以上"],

  e11: "您通常的单程通勤时间（住所到工作地点）",
  e11Choices: ["15 分钟以内", "15–30 分钟", "31–45 分钟", "46–60 分钟", "1 小时以上"],

  e12: "您家中是否有专门用于工作的房间或固定空间？",
  e12Choices: ["有", "没有"],

  ineligibleTitle: "感谢您的关注",
  ineligibleText:
    "本问卷仅面向目前在职的受雇人员。您可以在此提交，该份回答不会计入分析。感谢您抽出时间。",

  confirmation:
    "感谢您的参与。您的回答将用于一项面向法国与中国在职员工的工作组织方式研究。"
};
