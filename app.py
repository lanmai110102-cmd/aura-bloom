import json
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

from models import (
    db, TeamMember, ResultMetric, CaseStudy, CaseStudyMetric,
    OtherProject, WorkStep, WhyReason, SkillGroup, SiteSetting, Lead
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'aura_bloom.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("AURA_SECRET_KEY", "dev-secret-change-me")
ADMIN_PASSWORD = os.environ.get("AURA_ADMIN_PASSWORD", "aurabloom2026")

db.init_app(app)

with app.app_context():
    db.create_all()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def get_setting(key, lang, default=""):
    s = SiteSetting.query.get(key)
    if not s:
        return default
    if lang == "en" and s.value_en:
        return s.value_en
    return s.value


UI_TEXT = {
    "vi": {
        "nav_about": "Về chúng tôi", "nav_results": "Kết quả", "nav_case_studies": "Case Studies",
        "nav_team": "Team", "nav_how": "Quy trình", "nav_contact": "Liên hệ",
        "hero_title_pre": "Xây dựng thương hiệu của bạn với", "hero_title_accent": "Aura Bloom",
        "hero_cta_primary": "Xem Case Studies", "hero_cta_secondary": "Đặt lịch trao đổi",
        "stat1_label": "Doanh thu affiliate", "stat2_label": "Lượt xem IG/tháng", "stat3_label": "Cộng đồng creator",
        "s01_eyebrow": "01. Về chúng tôi", "s01_title": "Chúng tôi không chỉ quản lý content",
        "feature_title": "Chúng tôi giúp brand của bạn tăng trưởng thật, không chỉ “đẹp trên social”",
        "feature_1": "Phát triển concept và tái định vị thương hiệu cho SMEs và startups",
        "feature_2": "Chiến dịch tập trung chuyển đổi doanh số, không chỉ tăng nhận diện",
        "feature_3": "Kinh nghiệm thực chiến tại Việt Nam, Mỹ, Anh, Đức, Pháp, Úc",
        "s02_eyebrow": "02. Tổng hợp kết quả", "s02_title": "Results at a Glance",
        "th_project": "Dự án", "th_metric": "Chỉ số", "th_result": "Kết quả",
        "s03_eyebrow": "03. Case Studies", "s03_title": "Dự án nổi bật",
        "s03_lead": "Số liệu minh hoạ trực quan cho từng case study, lấy chính xác từ kết quả thực tế, không ước lượng.",
        "results_label": "Kết quả", "scope_label": "Triển khai",
        "challenge_label": "Thách thức", "insight_label": "Insight & Chiến lược",
        "image_credit_prefix": "Ảnh từ", "links_label": "Tài liệu & kênh chính thức",
        "other_projects_title": "Các dự án khác",
        "s04_eyebrow": "04. Team", "s04_title": "Thành viên", "team_cta": "Xem chi tiết →",
        "s05_eyebrow": "05. Quy trình làm việc", "s05_title": "How We Work",
        "s06_eyebrow": "06. Skills & Platforms", "s06_title": "Năng lực",
        "s07_eyebrow": "07. Tại sao chọn Aura Bloom", "s07_title": "Why Aura Bloom?",
        "contact_title": "Sẵn sàng để brand của bạn tăng trưởng thật?",
        "contact_desc": "Bước tiếp theo là một cuộc gọi khám phá 30 phút, không pitch deck, không áp lực. Aura Bloom sẽ phản hồi trong vòng 3 ngày làm việc.",
        "form_name": "Tên của bạn", "form_email": "Email", "form_company": "Công ty / Brand",
        "form_message": "Bạn cần hỗ trợ gì?", "form_submit": "Gửi yêu cầu",
        "admin_link": "Admin →",
    },
    "en": {
        "nav_about": "About", "nav_results": "Results", "nav_case_studies": "Case Studies",
        "nav_team": "Team", "nav_how": "How We Work", "nav_contact": "Contact",
        "hero_title_pre": "Build your brand with", "hero_title_accent": "Aura Bloom",
        "hero_cta_primary": "View Case Studies", "hero_cta_secondary": "Book a Call",
        "stat1_label": "Affiliate revenue", "stat2_label": "IG views/month", "stat3_label": "Creator community",
        "s01_eyebrow": "01. About Us", "s01_title": "We don't just manage content",
        "feature_title": "We help your brand grow for real, not just look good on social",
        "feature_1": "Concept development and brand repositioning for SMEs and startups",
        "feature_2": "Campaigns focused on sales conversion, not just visibility",
        "feature_3": "Hands-on experience in Vietnam, the US, UK, Germany, France, and Australia",
        "s02_eyebrow": "02. Results", "s02_title": "Results at a Glance",
        "th_project": "Project", "th_metric": "Metric", "th_result": "Result",
        "s03_eyebrow": "03. Case Studies", "s03_title": "Featured Work",
        "s03_lead": "Visual proof for each case study, drawn directly from real results, never estimated.",
        "results_label": "Results", "scope_label": "Execution",
        "challenge_label": "Challenge", "insight_label": "Insight & Strategy",
        "image_credit_prefix": "Image from", "links_label": "Documents & Official Channels",
        "other_projects_title": "Other Projects",
        "s04_eyebrow": "04. Team", "s04_title": "The Team", "team_cta": "View profile →",
        "s05_eyebrow": "05. How We Work", "s05_title": "How We Work",
        "s06_eyebrow": "06. Skills & Platforms", "s06_title": "Capabilities",
        "s07_eyebrow": "07. Why Aura Bloom", "s07_title": "Why Aura Bloom?",
        "contact_title": "Ready to make your brand grow for real?",
        "contact_desc": "The next step is a 30-minute discovery call, no pitch deck, no pressure. Aura Bloom replies within 3 business days.",
        "form_name": "Your name", "form_email": "Email", "form_company": "Company / Brand",
        "form_message": "What do you need help with?", "form_submit": "Send",
        "admin_link": "Admin →",
    },
}


def current_lang():
    return session.get("lang", "vi")


@app.context_processor
def inject_lang():
    return {"lang": current_lang(), "ui": UI_TEXT[current_lang()]}


@app.route("/lang/<code>")
def set_lang(code):
    if code in ("vi", "en"):
        session["lang"] = code
    return redirect(request.referrer or url_for("home"))


def localize_chart(chart, lang):
    out = dict(chart)
    if lang == "en":
        if chart.get("title_en"):
            out["title"] = chart["title_en"]
        if chart.get("labels_en"):
            out["labels"] = chart["labels_en"]
    return out


# ──────────────────────────────────────────────────────────────────────────
# PUBLIC SITE
# ──────────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    lang = current_lang()
    team = TeamMember.query.order_by(TeamMember.order).all()
    results = ResultMetric.query.order_by(ResultMetric.order).all()
    case_studies = CaseStudy.query.order_by(CaseStudy.order).all()

    for cs in case_studies:
        scope_raw = cs.scope_of_work_en if (lang == "en" and cs.scope_of_work_en) else cs.scope_of_work
        cs.scope_list = [x for x in (scope_raw or "").split("\n") if x.strip()]
        cs.display_subtitle = cs.subtitle_en if (lang == "en" and cs.subtitle_en) else cs.subtitle
        cs.display_category = cs.category_en if (lang == "en" and cs.category_en) else cs.category
        cs.display_challenge = cs.challenge_en if (lang == "en" and cs.challenge_en) else cs.challenge
        cs.display_insight = cs.insight_en if (lang == "en" and cs.insight_en) else cs.insight
        cs.display_results_note = cs.results_note_en if (lang == "en" and cs.results_note_en) else cs.results_note
        raw_charts = json.loads(cs.chart_data).get("charts", []) if cs.chart_data else []
        cs.charts = [localize_chart(c, lang) for c in raw_charts]
        if cs.results_table:
            rt = json.loads(cs.results_table)
            cs.display_table = {
                "headers": rt.get("headers_en") if (lang == "en" and rt.get("headers_en")) else rt.get("headers", []),
                "rows": rt.get("rows_en") if (lang == "en" and rt.get("rows_en")) else rt.get("rows", []),
            }
        else:
            cs.display_table = None
        for m in cs.metrics:
            m.display_label = m.label_en if (lang == "en" and m.label_en) else m.label
        for img in cs.images:
            img.display_caption = img.caption_en if (lang == "en" and img.caption_en) else img.caption
        grouped_links = {}
        for lk in cs.links:
            lk.display_group = lk.group_label_en if (lang == "en" and lk.group_label_en) else lk.group_label
            grouped_links.setdefault(lk.display_group, []).append(lk)
        cs.grouped_links = grouped_links

    grouped_cs = {}
    for cs in case_studies:
        grouped_cs.setdefault(cs.display_category, []).append(cs)

    other_projects = OtherProject.query.order_by(OtherProject.order).all()
    for p in other_projects:
        p.display_description = p.description_en if (lang == "en" and p.description_en) else p.description

    steps = WorkStep.query.order_by(WorkStep.order).all()
    for s in steps:
        s.display_title = s.title_en if (lang == "en" and s.title_en) else s.title
        s.display_description = s.description_en if (lang == "en" and s.description_en) else s.description

    why_reasons = WhyReason.query.order_by(WhyReason.order).all()
    for w in why_reasons:
        w.display_title = w.title_en if (lang == "en" and w.title_en) else w.title
        w.display_description = w.description_en if (lang == "en" and w.description_en) else w.description

    skills = SkillGroup.query.order_by(SkillGroup.order).all()
    for sk in skills:
        sk.display_label = sk.label_en if (lang == "en" and sk.label_en) else sk.label
        sk.display_items = sk.items_en if (lang == "en" and sk.items_en) else sk.items

    for r in results:
        r.display_metric = r.metric_en if (lang == "en" and r.metric_en) else r.metric
        r.display_project = r.project

    for t in team:
        t.display_role = t.role_en if (lang == "en" and t.role_en) else t.role
        t.display_bio = t.bio_en if (lang == "en" and t.bio_en) else t.bio

    return render_template(
        "index.html",
        team=team, results=results, grouped_cs=grouped_cs,
        other_projects=other_projects, steps=steps, why_reasons=why_reasons,
        skills=skills, about_text=get_setting("about_text", lang),
        why_sub=get_setting("why_sub", lang), contact_email=get_setting("contact_email", lang),
        contact_whatsapp=get_setting("contact_whatsapp", lang), closing_line=get_setting("closing_line", lang),
    )


@app.route("/team/<slug>")
def team_detail(slug):
    member = TeamMember.query.filter_by(detail_slug=slug).first_or_404()
    template_map = {
        "nhat-vy": "team_nhat_vy.html",
        "thanh-truc": "team_thanh_truc.html",
        "chi-lan": "team_chi_lan.html",
    }
    tpl = template_map.get(slug)
    if not tpl:
        return redirect(url_for("home"))
    return render_template(tpl, member=member)


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    company = request.form.get("company", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not email:
        flash("Vui lòng điền tên và email." if current_lang() == "vi" else "Please fill in your name and email.", "error")
        return redirect(url_for("home") + "#contact")
    lead = Lead(name=name, email=email, company=company, message=message)
    db.session.add(lead)
    db.session.commit()
    flash("Đã nhận được thông tin! Aura Bloom sẽ liên hệ lại sớm." if current_lang() == "vi"
          else "Got it! Aura Bloom will be in touch soon.", "success")
    return redirect(url_for("home") + "#contact")


# ──────────────────────────────────────────────────────────────────────────
# ADMIN
# ──────────────────────────────────────────────────────────────────────────
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash("Sai mật khẩu.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html",
                            n_cs=CaseStudy.query.count(),
                            n_projects=OtherProject.query.count(),
                            n_team=TeamMember.query.count(),
                            n_leads=Lead.query.count(),
                            n_results=ResultMetric.query.count())


# ---- Case Studies CRUD ----
@app.route("/admin/case-studies")
@login_required
def admin_case_studies():
    items = CaseStudy.query.order_by(CaseStudy.order).all()
    return render_template("admin/case_studies.html", items=items)


@app.route("/admin/case-studies/new", methods=["GET", "POST"])
@login_required
def admin_case_study_new():
    if request.method == "POST":
        cs = CaseStudy(
            number=request.form["number"], category=request.form["category"],
            title=request.form["title"], subtitle=request.form.get("subtitle", ""),
            scope_of_work=request.form.get("scope_of_work", ""),
            results_note=request.form.get("results_note", ""),
            image_url=request.form.get("image_url", ""),
            image_credit=request.form.get("image_credit", ""),
            order=int(request.form.get("order") or 0),
        )
        db.session.add(cs)
        db.session.commit()
        flash("Đã tạo case study.", "success")
        return redirect(url_for("admin_case_studies"))
    return render_template("admin/case_study_form.html", item=None)


@app.route("/admin/case-studies/<int:cs_id>/edit", methods=["GET", "POST"])
@login_required
def admin_case_study_edit(cs_id):
    cs = CaseStudy.query.get_or_404(cs_id)
    if request.method == "POST":
        cs.number = request.form["number"]
        cs.category = request.form["category"]
        cs.title = request.form["title"]
        cs.subtitle = request.form.get("subtitle", "")
        cs.scope_of_work = request.form.get("scope_of_work", "")
        cs.results_note = request.form.get("results_note", "")
        cs.image_url = request.form.get("image_url", "")
        cs.image_credit = request.form.get("image_credit", "")
        cs.order = int(request.form.get("order") or 0)
        db.session.commit()
        flash("Đã lưu thay đổi.", "success")
        return redirect(url_for("admin_case_studies"))
    return render_template("admin/case_study_form.html", item=cs)


@app.route("/admin/case-studies/<int:cs_id>/delete", methods=["POST"])
@login_required
def admin_case_study_delete(cs_id):
    cs = CaseStudy.query.get_or_404(cs_id)
    db.session.delete(cs)
    db.session.commit()
    flash("Đã xoá case study.", "success")
    return redirect(url_for("admin_case_studies"))


# ---- Other Projects CRUD ----
@app.route("/admin/projects", methods=["GET", "POST"])
@login_required
def admin_projects():
    if request.method == "POST":
        p = OtherProject(name=request.form["name"], description=request.form["description"],
                          order=int(request.form.get("order") or 0))
        db.session.add(p)
        db.session.commit()
        flash("Đã thêm dự án.", "success")
        return redirect(url_for("admin_projects"))
    items = OtherProject.query.order_by(OtherProject.order).all()
    return render_template("admin/projects.html", items=items)


@app.route("/admin/projects/<int:p_id>/delete", methods=["POST"])
@login_required
def admin_project_delete(p_id):
    p = OtherProject.query.get_or_404(p_id)
    db.session.delete(p)
    db.session.commit()
    flash("Đã xoá.", "success")
    return redirect(url_for("admin_projects"))


# ---- Team CRUD ----
@app.route("/admin/team", methods=["GET", "POST"])
@login_required
def admin_team():
    if request.method == "POST":
        t = TeamMember(
            name=request.form["name"], role=request.form["role"], bio=request.form.get("bio", ""),
            email=request.form.get("email", ""), phone=request.form.get("phone", ""),
            initials=request.form.get("initials", ""), detail_slug=request.form.get("detail_slug", ""),
            order=int(request.form.get("order") or 0),
        )
        db.session.add(t)
        db.session.commit()
        flash("Đã thêm thành viên.", "success")
        return redirect(url_for("admin_team"))
    items = TeamMember.query.order_by(TeamMember.order).all()
    return render_template("admin/team.html", items=items)


@app.route("/admin/team/<int:t_id>/delete", methods=["POST"])
@login_required
def admin_team_delete(t_id):
    t = TeamMember.query.get_or_404(t_id)
    db.session.delete(t)
    db.session.commit()
    flash("Đã xoá.", "success")
    return redirect(url_for("admin_team"))


# ---- Results CRUD ----
@app.route("/admin/results", methods=["GET", "POST"])
@login_required
def admin_results():
    if request.method == "POST":
        r = ResultMetric(metric=request.form["metric"], result=request.form["result"],
                          project=request.form["project"], order=int(request.form.get("order") or 0))
        db.session.add(r)
        db.session.commit()
        flash("Đã thêm chỉ số.", "success")
        return redirect(url_for("admin_results"))
    items = ResultMetric.query.order_by(ResultMetric.order).all()
    return render_template("admin/results.html", items=items)


@app.route("/admin/results/<int:r_id>/delete", methods=["POST"])
@login_required
def admin_result_delete(r_id):
    r = ResultMetric.query.get_or_404(r_id)
    db.session.delete(r)
    db.session.commit()
    flash("Đã xoá.", "success")
    return redirect(url_for("admin_results"))


# ---- Leads (read-only) ----
@app.route("/admin/leads")
@login_required
def admin_leads():
    items = Lead.query.order_by(Lead.created_at.desc()).all()
    return render_template("admin/leads.html", items=items)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)
