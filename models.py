from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(160), nullable=False)
    role_en = db.Column(db.String(160), default="")
    bio = db.Column(db.Text, default="")
    bio_en = db.Column(db.Text, default="")
    email = db.Column(db.String(120), default="")
    phone = db.Column(db.String(60), default="")
    initials = db.Column(db.String(4), default="")
    detail_slug = db.Column(db.String(60), default="")
    photo_url = db.Column(db.String(300), default="")
    order = db.Column(db.Integer, default=0)


class ResultMetric(db.Model):
    """Bảng Results at a Glance"""
    id = db.Column(db.Integer, primary_key=True)
    metric = db.Column(db.String(200), nullable=False)
    metric_en = db.Column(db.String(200), default="")
    result = db.Column(db.String(120), nullable=False)
    result_en = db.Column(db.String(120), default="")
    project = db.Column(db.String(120), nullable=False)
    order = db.Column(db.Integer, default=0)


class CaseStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(4), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    category_en = db.Column(db.String(80), default="")
    title = db.Column(db.String(160), nullable=False)
    title_en = db.Column(db.String(160), default="")
    subtitle = db.Column(db.String(220), default="")
    subtitle_en = db.Column(db.String(220), default="")
    challenge = db.Column(db.Text, default="")          # optional "Thách thức" intro
    challenge_en = db.Column(db.Text, default="")
    insight = db.Column(db.Text, default="")             # optional "Insight & Chiến lược"
    insight_en = db.Column(db.Text, default="")
    scope_of_work = db.Column(db.Text, default="")     # newline-separated bullets ("Triển khai")
    scope_of_work_en = db.Column(db.Text, default="")
    results_note = db.Column(db.Text, default="")       # optional qualitative note
    results_note_en = db.Column(db.Text, default="")
    results_table = db.Column(db.Text, default="")       # optional JSON: {headers, headers_en, rows}
    chart_type = db.Column(db.String(20), default="")   # "bar", "growth", "table", ""
    chart_data = db.Column(db.Text, default="")          # JSON string
    image_url = db.Column(db.String(400), default="")    # ảnh thật từ portfolio gốc
    image_credit = db.Column(db.String(200), default="") # nguồn ảnh (Canva design / PDF)
    order = db.Column(db.Integer, default=0)

    metrics = db.relationship("CaseStudyMetric", backref="case_study",
                               cascade="all, delete-orphan", order_by="CaseStudyMetric.order")
    images = db.relationship("CaseStudyImage", backref="case_study",
                              cascade="all, delete-orphan", order_by="CaseStudyImage.order")
    links = db.relationship("CaseStudyLink", backref="case_study",
                             cascade="all, delete-orphan", order_by="CaseStudyLink.order")


class CaseStudyLink(db.Model):
    """Link tài liệu/kênh chính thức của 1 case study, hiển thị dạng pill button"""
    id = db.Column(db.Integer, primary_key=True)
    case_study_id = db.Column(db.Integer, db.ForeignKey("case_study.id"), nullable=False)
    group_label = db.Column(db.String(80), default="")
    group_label_en = db.Column(db.String(80), default="")
    label = db.Column(db.String(160), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(10), default="")
    order = db.Column(db.Integer, default=0)


class CaseStudyImage(db.Model):
    """Ảnh thật cho gallery lướt ngang của 1 case study"""
    id = db.Column(db.Integer, primary_key=True)
    case_study_id = db.Column(db.Integer, db.ForeignKey("case_study.id"), nullable=False)
    image_url = db.Column(db.String(400), nullable=False)
    caption = db.Column(db.String(300), default="")
    caption_en = db.Column(db.String(300), default="")
    order = db.Column(db.Integer, default=0)


class CaseStudyMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_study_id = db.Column(db.Integer, db.ForeignKey("case_study.id"), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    label_en = db.Column(db.String(200), default="")
    value = db.Column(db.String(80), nullable=False)
    order = db.Column(db.Integer, default=0)


class OtherProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, default="")
    order = db.Column(db.Integer, default=0)


class WorkStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(4), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    title_en = db.Column(db.String(160), default="")
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, default="")
    order = db.Column(db.Integer, default=0)


class WhyReason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    title_en = db.Column(db.String(160), default="")
    description = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, default="")
    order = db.Column(db.Integer, default=0)


class SkillGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), nullable=False)
    label_en = db.Column(db.String(80), default="")
    items = db.Column(db.Text, nullable=False)  # "·" separated
    items_en = db.Column(db.Text, default="")
    order = db.Column(db.Integer, default=0)


class SiteSetting(db.Model):
    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.Text, default="")
    value_en = db.Column(db.Text, default="")


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(160), default="")
    message = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
