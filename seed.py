import json
from app import app
from models import (
    db, TeamMember, ResultMetric, CaseStudy, CaseStudyMetric, CaseStudyImage, CaseStudyLink,
    OtherProject, WorkStep, WhyReason, SkillGroup, SiteSetting
)


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ---------- Team ----------
        db.session.add_all([
            TeamMember(
                name="Nguyễn Hoàng Nhật Vy",
                role="Team Lead · Content Strategist & Social Media Manager",
                role_en="Team Lead · Content Strategist & Social Media Manager",
                bio="Chiến lược nội dung đa kênh, personal branding cho executives, kinh nghiệm thị trường Mỹ, Anh, Úc, Đức, Pháp.",
                bio_en="Multi-channel content strategy, personal branding for executives, hands-on experience in the US, UK, Australia, Germany, and France.",
                email="nhatvyng.forwork@gmail.com", phone="0942 468 708",
                initials="NV", detail_slug="nhat-vy", photo_url="team/nhat-vy.jpg", order=1
            ),
            TeamMember(
                name="Thanh Trúc (Chloe Nguyen)",
                role="Content, Cộng đồng & Marketing Mạng Xã Hội · 3+ năm",
                role_en="Content, Community & Social Media Marketing · 3+ years",
                bio="Marketing planning, seasonal campaigns, KOL/KOC coordination, vận hành cộng đồng creator 10.000+ thành viên.",
                bio_en="Marketing planning, seasonal campaigns, KOL/KOC coordination, operating a creator community of 10,000+ members.",
                email="thanhtrucnguyen0106@gmail.com", phone="0365 334 549",
                initials="TT", detail_slug="thanh-truc", order=2
            ),
            TeamMember(
                name="Mai Nguyễn Chi Lan",
                role="Brand Strategist & Content Marketing Executive · 2+ năm",
                role_en="Brand Strategist & Content Marketing Executive · 2+ years",
                bio="Brand building từ số 0, storytelling, KOL/KOC management, HubSpot Certified.",
                bio_en="Brand building from zero, storytelling, KOL/KOC management, HubSpot Certified.",
                email="lanmai.110102@gmail.com", phone="0382 590 011",
                initials="CL", detail_slug="chi-lan", order=3
            ),
        ])

        # ---------- Results at a Glance ----------
        results = [
            ("Doanh thu affiliate tạo ra", "Affiliate revenue generated", "$75.000", "Wellness Nest"),
            ("Doanh thu cao nhất từ một creator", "Highest revenue from a single creator", "$18.600+ (peak tháng 12)", "Wellness Nest"),
            ("Doanh thu chiến dịch theo mùa", "Seasonal campaign revenue", "~400 triệu VNĐ (gấp 3 lần)", "Suri's Concept"),
            ("Doanh thu nền tháng ngoài cao điểm", "Baseline revenue in off-peak months", "~200 triệu VNĐ/tháng", "Suri's Concept"),
            ("Lượt xem Instagram organic mỗi tháng", "Organic Instagram views per month", "786.100", "BABE Co. Agency IG"),
            ("Tăng trưởng lượt xem IG theo tháng", "Month-on-month IG view growth", "+64,5%", "BABE Co. Agency IG"),
            ("Lượt xem hashtag trong 30 ngày", "Hashtag views within 30 days", "12.000.000 (#theauravn)", "The Aura"),
            ("Tăng trưởng doanh thu Shopee trong 1 tháng", "Shopee revenue growth in 1 month", "514,87%", "The Aura"),
            ("Tăng trưởng email list (tháng 3 so với tháng 1)", "Email list growth (month 3 vs month 1)", "Tăng 329% trong 2 tháng", "VNCreatorpreneur"),
            ("Cộng đồng creator xây dựng được", "Creator community built", "10.000+ thành viên", "The BABE Playground"),
            ("Kênh Instagram đạt 10K+ followers mỗi kênh", "Instagram channels with 10K+ followers each", "30+", "BABE Co. US Market"),
            ("Doanh thu tháng ra mắt F&B", "Launch month revenue (F&B)", "~100 triệu+ VNĐ", "Cháo Vịt Liên"),
            ("Lượt xem nội dung bất động sản", "Real estate content views", "Lên đến 545.000/video", "Nhà Phố Giá Thật"),
            ("Tăng trưởng follower TikTok trong 4 tháng", "TikTok follower growth in 4 months", "2.400", "Nhà Phố Giá Thật"),
        ]
        for i, (m, m_en, r, p) in enumerate(results):
            db.session.add(ResultMetric(metric=m, metric_en=m_en, result=r, project=p, order=i))

        # ---------- Case Studies ----------
        cs1 = CaseStudy(
            number="01", category="Doanh thu", category_en="Revenue", title="Wellness Nest",
            subtitle="Thực phẩm chức năng · Multi-Market Affiliate · Mỹ / Anh / Đức / Pháp",
            subtitle_en="Health Supplements · Multi-Market Affiliate · US / UK / Germany / France",
            scope_of_work="\n".join([
                "Tuyển dụng và phân phối creator tại Mỹ, Anh, Đức và Pháp với brief định vị riêng cho từng thị trường.",
                "Triển khai nội dung bằng tiếng Anh, tiếng Đức và tiếng Pháp trên TikTok, YouTube Shorts, Instagram và Threads.",
                "Coaching creator về cách định vị sản phẩm để tự tạo doanh thu ổn định mà không cần brief liên tục.",
                "Theo dõi hiệu suất từng creator và phản hồi tối ưu hóa định kỳ 2 tuần một lần.",
            ]),
            scope_of_work_en="\n".join([
                "Recruited and placed creators in the US, UK, Germany, and France with market-specific positioning briefs.",
                "Deployed content in English, German, and French across TikTok, YouTube Shorts, Instagram, and Threads.",
                "Coached creators on product positioning so they could generate steady revenue without constant briefing.",
                "Tracked each creator's performance with optimization feedback every two weeks.",
            ]),
            order=1
        )
        cs1.metrics = [
            CaseStudyMetric(label="Tổng doanh thu affiliate trên tất cả thị trường",
                             label_en="Total affiliate revenue across all markets", value="$75.000", order=1),
            CaseStudyMetric(label="Doanh thu cao nhất từ một creator (peak tháng 12)",
                             label_en="Highest revenue from a single creator (December peak)", value="$18.600+", order=2),
            CaseStudyMetric(label="Số thị trường kích hoạt đồng thời",
                             label_en="Markets activated simultaneously", value="Mỹ · Anh · Đức · Pháp", order=3),
        ]
        cs1.images = [
            CaseStudyImage(image_url="wellness-proof/proof-1.png",
                            caption="Doanh thu cao nhất từ một creator: $18.600+ (TinTin, 282 đơn hàng)",
                            caption_en="Highest revenue from a single creator: $18,600+ (TinTin, 282 orders)", order=1),
            CaseStudyImage(image_url="wellness-proof/proof-2.png",
                            caption="Doanh thu theo creator: TinTin $15.174,60 · Mani $3.027,18 · Hồ Hảo $2.420,91 · Winnie $1.930,53",
                            caption_en="Revenue by creator: TinTin $15,174.60 · Mani $3,027.18 · Hồ Hảo $2,420.91 · Winnie $1,930.53", order=2),
            CaseStudyImage(image_url="wellness-proof/proof-3.png",
                            caption="Doanh thu theo creator (tiếp theo): Nguyễn Minh Cường $4.763,27 · ANH THU $4.260,48 · Doãn Quang Linh $3.842,49 · Minh Châu $3.015,42 · minne $1.951,55",
                            caption_en="Revenue by creator (cont.): Nguyễn Minh Cường $4,763.27 · ANH THU $4,260.48 · Doãn Quang Linh $3,842.49 · Minh Châu $3,015.42 · minne $1,951.55", order=3),
            CaseStudyImage(image_url="wellness-proof/proof-4.jpg",
                            caption="Video viral trên TikTok cho Wellness Nest: từ 568,4K đến 7,8M lượt xem",
                            caption_en="Viral TikTok videos for Wellness Nest: from 568.4K to 7.8M views", order=4),
            CaseStudyImage(image_url="wellness-proof/proof-5.jpg",
                            caption="Kênh Instagram đa thị trường: Đức, Pháp, Mỹ/Anh",
                            caption_en="Multi-market Instagram channels: Germany, France, US/UK", order=5),
            CaseStudyImage(image_url="wellness-proof/proof-6.png",
                            caption="Kênh Threads (12,3K followers) và Instagram (56,6K followers)",
                            caption_en="Threads channel (12.3K followers) and Instagram (56.6K followers)", order=6),
        ]

        cs2 = CaseStudy(
            number="02", category="Doanh thu", category_en="Revenue", title="Suri's Concept",
            subtitle="Hoa khô · Chiến dịch theo mùa + Quản lý mạng xã hội · TP.HCM",
            subtitle_en="Dried Flowers · Seasonal Campaign + Full Social Management · Ho Chi Minh City",
            scope_of_work="\n".join([
                "Lên kế hoạch chiến dịch đầy đủ cho 20/10 và 8/3: concept, content direction, brief và booking KOL/KOC.",
                "Quản lý nội dung hàng ngày trên TikTok, Instagram, Facebook và Threads, giữ giọng điệu nhất quán trên tất cả nền tảng.",
                "Tối ưu giữa chiến dịch: phân bổ lại ngân sách seeding về nhóm nội dung hiệu quả nhất ngay sau ngày 3.",
                "Chiến lược nội dung ngoài mùa cao điểm để duy trì doanh thu nền ổn định giữa các chiến dịch.",
            ]),
            scope_of_work_en="\n".join([
                "Built full campaign plans for 20/10 and 8/3: concept, content direction, KOL/KOC briefing and booking.",
                "Managed daily content across TikTok, Instagram, Facebook, and Threads with a consistent voice on every platform.",
                "Optimized mid-campaign by reallocating seeding budget to the best-performing content within the first 3 days.",
                "Ran an off-peak content strategy to keep baseline revenue stable between campaigns.",
            ]),
            order=2
        )
        cs2.metrics = [
            CaseStudyMetric(label="20/10 (2025): gấp 3 lần kỷ lục cũ", label_en="20/10 (2025): 3x the brand's previous record",
                             value="~400.000.000 VNĐ", order=1),
            CaseStudyMetric(label="8/3 (2026): đạt mục tiêu peak", label_en="8/3 (2026): hit peak target",
                             value="~300.000.000 VNĐ", order=2),
            CaseStudyMetric(label="Ngoài cao điểm: doanh thu nền duy trì", label_en="Off-peak: stable baseline revenue",
                             value="~200.000.000 VNĐ", order=3),
        ]
        cs2.images = [
            CaseStudyImage(image_url="suri-proof/proof-1.png",
                            caption="Bảng theo dõi doanh thu hàng ngày: 5.980 khách inbox, 370 đơn chốt, 375.405.000đ, tỉ lệ chốt đơn 6,19%",
                            caption_en="Daily revenue tracker: 5,980 inbox leads, 370 orders closed, 375,405,000 VND, 6.19% close rate", order=1),
            CaseStudyImage(image_url="suri-proof/proof-2.jpg",
                            caption="Kịch bản content thực tế: storytelling theo cảm xúc cho từng dòng sản phẩm hoa khô",
                            caption_en="Real content scripts: emotion-driven storytelling for each dried-flower product line", order=2),
            CaseStudyImage(image_url="suri-proof/proof-6.jpg",
                            caption="Sản phẩm thực tế: hộp hoa khô hình tim cho chiến dịch PRE-ORDER 20/10",
                            caption_en="Real product photos: heart-shaped dried-flower boxes for the 20/10 PRE-ORDER campaign", order=3),
        ]
        cs2.links = [
            CaseStudyLink(group_label="Tài liệu", group_label_en="Documents",
                           label="Marketing Proposal · 20/10 (2025)", icon="📄",
                           url="https://drive.google.com/file/d/1H09q_ZoApm9GttKg4-tXd-XelwCfc4nX/view", order=1),
            CaseStudyLink(group_label="Tài liệu", group_label_en="Documents",
                           label="Marketing Proposal · 8/3 (2026)", icon="📄",
                           url="https://drive.google.com/file/d/1Zrlt9dSehh2BZIAYWGHoxtu8pCxwMxxp/view", order=2),
            CaseStudyLink(group_label="Tài liệu", group_label_en="Documents",
                           label="Content Plan", icon="📊",
                           url="https://docs.google.com/spreadsheets/d/1pSX8Oy0D5xrUisrdGT5uFr1WPETN0OIksh5CI8HUS5Y/edit?gid=2058619132#gid=2058619132", order=3),
            CaseStudyLink(group_label="Kênh chính thức", group_label_en="Official Channels",
                           label="Facebook", icon="📘",
                           url="https://www.facebook.com/tiemhoakhosuri/photos", order=4),
            CaseStudyLink(group_label="Kênh chính thức", group_label_en="Official Channels",
                           label="Instagram", icon="📷",
                           url="https://www.instagram.com/tiemhoakhosuri/", order=5),
            CaseStudyLink(group_label="Kênh chính thức", group_label_en="Official Channels",
                           label="TikTok", icon="🎵",
                           url="https://www.tiktok.com/@tiemhoakhosuri", order=6),
        ]

        cs3 = CaseStudy(
            number="03", category="Personal Brand", category_en="Personal Brand", title="Tiến Trần & AMAZ",
            subtitle="Kiến trúc cao cấp · Personal Brand + Mạng xã hội thương hiệu · Việt Nam",
            subtitle_en="Luxury Architecture · Personal Brand + Brand Social Media · Vietnam",
            scope_of_work="\n".join([
                "Xây dựng và quản lý nội dung cho cả personal brand của chủ sở hữu (Tiến Trần) và các kênh thương hiệu AMAZ.",
                "Sản xuất nội dung cho các dự án biệt thự, căn hộ hạng sang và dinh thự, từ phát triển concept đến giám sát thực thi video.",
                "Xây dựng creative direction để duy trì định vị cao cấp nhất quán trên tất cả điểm chạm thương hiệu.",
                "Quản lý lịch đăng bài, tương tác cộng đồng và giọng nói thương hiệu xuyên suốt các nền tảng.",
            ]),
            scope_of_work_en="\n".join([
                "Built and managed content for both the founder's personal brand (Tiến Trần) and the AMAZ brand channels.",
                "Produced content for villa, luxury residence, and mansion projects, from concept development to video execution oversight.",
                "Set the creative direction to keep premium positioning consistent across every brand touchpoint.",
                "Managed posting schedule, community engagement, and brand voice across all platforms.",
            ]),
            results_note="Định vị thương hiệu kiến trúc cao cấp được xây dựng và duy trì nhất quán trên tất cả kênh. "
                          "Nội dung xây dựng uy tín và tầm ảnh hưởng trong phân khúc bất động sản hạng sang.",
            results_note_en="A consistent premium architecture positioning was built and maintained across every channel. "
                             "The content built authority and influence within the luxury real estate segment.",
            order=3
        )
        cs3.images = [
            CaseStudyImage(image_url="amaz-proof/proof-2.jpg",
                            caption="HM Mansion, Hạ Long: cập nhật tiến độ thi công thực tế",
                            caption_en="HM Mansion, Hạ Long: real construction progress update", order=1),
            CaseStudyImage(image_url="amaz-proof/proof-3.jpg",
                            caption="RESORT IN HOME: bộ sưu tập các dự án villa/dinh thự đã hoàn thiện",
                            caption_en="RESORT IN HOME: collection of completed villa and mansion projects", order=2),
            CaseStudyImage(image_url="amaz-proof/proof-4.jpg",
                            caption="AMAZ x Phan Anh Luxury Living: sự kiện tại Milan, Italy",
                            caption_en="AMAZ x Phan Anh Luxury Living: event in Milan, Italy", order=3),
            CaseStudyImage(image_url="amaz-proof/proof-5.png",
                            caption="Content plan thực tế: chủ đề, format, dự án và lịch lên sóng theo tháng",
                            caption_en="Real content plan: topics, format, project, and monthly publishing schedule", order=4),
            CaseStudyImage(image_url="amaz-proof/proof-6.png",
                            caption="Editing guideline chi tiết cho từng video: cảnh quay, source, text, nhạc",
                            caption_en="Detailed editing guideline per video: shots, source footage, on-screen text, music", order=5),
            CaseStudyImage(image_url="amaz-proof/proof-7.jpg",
                            caption="Định hướng xây kênh: target audience, insight, định hình kênh và USP",
                            caption_en="Channel strategy doc: target audience, insight, channel positioning, and USP", order=6),
        ]
        cs3.links = [
            CaseStudyLink(group_label="Tài liệu", group_label_en="Documents",
                           label="Action Plan", icon="📊",
                           url="https://docs.google.com/spreadsheets/d/1QZDOIdpDRKQPIhue2QrjbBhLDzc9PjUR/edit?gid=1550833022#gid=1550833022", order=1),
            CaseStudyLink(group_label="Kênh chính thức", group_label_en="Official Channels",
                           label="Facebook", icon="📘",
                           url="https://www.facebook.com/amazgroupvn", order=2),
        ]

        cs4 = CaseStudy(
            number="04", category="Personal Brand", category_en="Personal Brand", title="Nhà Phố Giá Thật",
            subtitle="Bất động sản · Personal Branding & Chiến lược nội dung · Việt Nam",
            subtitle_en="Real Estate · Personal Branding & Content Strategy · Vietnam",
            scope_of_work="\n".join([
                "Xây dựng kế hoạch nội dung trên TikTok, YouTube Shorts và Facebook định vị chủ sở hữu là chuyên gia bất động sản nhà phố.",
                "Sản xuất nội dung giáo dục (cách tính giá, dấu hiệu rủi ro cần lưu ý, kiến thức đàm phán) và nội dung xây dựng niềm tin.",
                "Điều chỉnh định dạng và tone riêng cho từng nền tảng: nội dung ngắn trên TikTok/Shorts, nội dung sâu hơn trên Facebook.",
                "Theo dõi chủ đề và định dạng nào mang lại nhiều lượt xem và tăng follower nhất, ưu tiên sản xuất nội dung tương tự.",
            ]),
            scope_of_work_en="\n".join([
                "Built a content plan across TikTok, YouTube Shorts, and Facebook positioning the owner as a townhouse real estate expert.",
                "Produced educational content (pricing, red flags, negotiation basics) alongside trust-building content.",
                "Adapted format and tone per platform: short-form education on TikTok/Shorts, deeper context on Facebook.",
                "Tracked which topics and formats drove the most views and follower growth, then prioritized similar content.",
            ]),
            order=4
        )
        cs4.images = [
            CaseStudyImage(image_url="nhapho-proof/proof-1.jpg",
                            caption="Lưới video TikTok thực tế: nội dung giáo dục và câu chuyện bất động sản, lượt xem từ 5,6K đến 545,1K",
                            caption_en="Real TikTok video grid: educational and real-estate storytelling content, views from 5.6K to 545.1K", order=1),
            CaseStudyImage(image_url="nhapho-proof/proof-2.jpg",
                            caption="Video về tháp đồng hồ chợ Bến Thành: 11,9K lượt thích, 103 bình luận, 838 lượt lưu",
                            caption_en="Video about the Bến Thành market clock tower: 11.9K likes, 103 comments, 838 saves", order=2),
        ]
        cs4.links = [
            CaseStudyLink(group_label="Tài liệu", group_label_en="Documents",
                           label="Content Plan", icon="📊",
                           url="https://drive.google.com/file/d/1mnsf8nAMuSBOjSu9L6BgYaUAVhIHGgcZ/view", order=1),
            CaseStudyLink(group_label="Kênh chính thức", group_label_en="Official Channels",
                           label="TikTok", icon="🎵",
                           url="https://www.tiktok.com/@nhaphogiathat", order=2),
        ]
        cs4.metrics = [
            CaseStudyMetric(label="Tăng trưởng follower TikTok trong 4 tháng",
                             label_en="TikTok follower growth in 4 months", value="2.400", order=1),
            CaseStudyMetric(label="Lượt xem cao nhất mỗi video",
                             label_en="Highest views per video", value="545.000", order=2),
        ]

        cs5 = CaseStudy(
            number="05", category="Content · Traffic · Concept", category_en="Content · Traffic · Concept", title="Mastr Mode",
            subtitle="Hệ thống đa kênh Instagram · Thị trường Mỹ · Affiliate Digital Product",
            subtitle_en="Multi-Channel Instagram System · US Market · Affiliate Digital Product",
            scope_of_work="\n".join([
                "Xây dựng và vận hành hệ thống 100+ tài khoản Instagram tại thị trường Mỹ, mỗi creator quản lý đồng thời 2 đến 10 kênh.",
                "Trang bị cho creator trong cộng đồng mindset, kỹ năng và công cụ để tự sản xuất viral content và high-conversion media.",
            ]),
            scope_of_work_en="\n".join([
                "Built and operated a 100+ account Instagram system in the US market, with each creator managing 2 to 10 channels at once.",
                "Equipped community creators with the mindset, skills, and tools to produce viral content and high-conversion media on their own.",
            ]),
            order=5
        )
        cs5.metrics = [
            CaseStudyMetric(label="Doanh thu trung bình hàng tháng trên toàn hệ thống kênh",
                             label_en="Average monthly revenue across the channel network", value="50-100tr+ VNĐ", order=1),
            CaseStudyMetric(label="Kênh đạt 10.000+ followers", label_en="Channels with 10,000+ followers", value="30+", order=2),
            CaseStudyMetric(label="Kênh đạt 1.000+ followers", label_en="Channels with 1,000+ followers", value="45+", order=3),
            CaseStudyMetric(label="Satellite channels đang hoạt động và tăng trưởng",
                             label_en="Satellite channels active and growing", value="270+", order=4),
        ]
        cs5.images = [
            CaseStudyImage(image_url="mastr-proof/proof-1.jpg",
                            caption="6 tài khoản Instagram thật trong hệ thống: 31,6K đến 87,4K followers mỗi kênh",
                            caption_en="6 real Instagram accounts in the system: 31.6K to 87.4K followers each", order=1),
            CaseStudyImage(image_url="mastr-proof/proof-2.jpg",
                            caption="Video viral nhất trong hệ thống: từ 2,9M đến 20,5M lượt xem",
                            caption_en="Top-performing videos across the system: from 2.9M to 20.5M views", order=2),
            CaseStudyImage(image_url="mastr-proof/proof-3.jpg",
                            caption="Video viral khác trong hệ thống: từ 1M đến 5,6M lượt xem",
                            caption_en="More viral videos across the system: from 1M to 5.6M views", order=3),
        ]

        cs6 = CaseStudy(
            number="06", category="Content · Traffic · Concept", category_en="Content · Traffic · Concept",
            title="BABE Co. Tăng trưởng kênh Instagram",
            subtitle="Marketing Agency · Organic Instagram Growth · Đối tượng B2B",
            subtitle_en="Marketing Agency · Organic Instagram Growth · B2B Audience",
            challenge="BABE Co. cần kênh Instagram riêng để thu hút khách hàng B2B và chứng minh năng lực marketing thực chiến. "
                       "Điểm khởi đầu: reach gần bằng 0 (vài chục mỗi tháng), không có định hướng nội dung, không có giọng nói thương hiệu. "
                       "Đối tượng là chủ doanh nghiệp, startup founders và brand managers, những người hoài nghi và bỏ qua content marketing chung chung.",
            challenge_en="BABE Co. needed its own Instagram channel to attract B2B clients and prove real marketing capability. "
                          "Starting point: near-zero reach (a few dozen per month), no content direction, no brand voice. "
                          "The audience was business owners, startup founders, and brand managers, a skeptical group that ignores generic marketing content.",
            insight="Sau khi audit những nội dung mà đối tượng này thực sự tương tác, chúng tôi tìm ra một pattern nhất quán: "
                    "họ lưu và chia sẻ nội dung nói về thực tế kinh doanh, gồm nỗi sợ thất bại, áp lực khi xây dựng thứ gì đó, chi phí cảm xúc của khởi nghiệp. "
                    "Content tips marketing thuần túy không tạo ra kết nối cảm xúc nào. "
                    "Quyết định pivot: định vị kênh là tiếng nói nói thật về kinh doanh, dùng storytelling mạnh, thẳng thắn, "
                    "đúng với cách người trẻ Việt Nam đang xây dựng sự nghiệp thực sự muốn nghe.",
            insight_en="After auditing what this audience actually engaged with, we found a consistent pattern: "
                       "they saved and shared content about business reality, including fear of failure, the pressure of building something, "
                       "and the emotional cost of entrepreneurship. Pure marketing tips created zero emotional connection. "
                       "The pivot: position the channel as a voice that tells the truth about business, using strong, direct storytelling "
                       "that matched how young Vietnamese people building their careers actually wanted to hear it.",
            scope_of_work="\n".join([
                "Chuyển hoàn toàn sang nội dung storytelling-first, không tips, không how-to, chỉ góc nhìn thực về mindset kinh doanh và tiền bạc.",
                "Format chủ đạo: Reels text-on-dark-background và carousel, tỷ lệ save và share cao, thân thiện với thuật toán.",
                "Duy trì tần suất đăng bài nhất quán; A/B test caption hàng tuần để xác định góc độ nào resonates nhất.",
                "Theo dõi reach, saves và shares (không chỉ likes) làm tín hiệu hiệu suất chính.",
            ]),
            scope_of_work_en="\n".join([
                "Shifted entirely to storytelling-first content: no tips, no how-tos, just real perspectives on business mindset and money.",
                "Primary formats: text-on-dark-background Reels and carousels, with high save and share rates that are algorithm-friendly.",
                "Maintained a consistent posting cadence; A/B tested captions weekly to find which angles resonated most.",
                "Tracked reach, saves, and shares (not just likes) as the primary performance signal.",
            ]),
            results_table=json.dumps({
                "headers": ["Chỉ số", "Trước (ban đầu)", "Tháng 8/2025", "Tháng 9/2025", "Thay đổi (T8→T9)"],
                "headers_en": ["Metric", "Before (baseline)", "August 2025", "September 2025", "Change (Aug→Sep)"],
                "rows": [
                    ["Lượt xem/tháng", "~vài trăm", "477.900", "786.100", "+64,5%"],
                    ["Reach/tháng", "~vài chục", "104.400", "145.300", "+39,3%"],
                    ["Tương tác", "không đáng kể", "14.600", "21.200", "+45,3%"],
                    ["Bài viral cao nhất", "N/A", "N/A", "194.000 lượt xem", "N/A"],
                ],
                "rows_en": [
                    ["Monthly views", "~hundreds", "477,900", "786,100", "+64.5%"],
                    ["Monthly reach", "~dozens", "104,400", "145,300", "+39.3%"],
                    ["Interactions", "minimal", "14,600", "21,200", "+45.3%"],
                    ["Top viral post", "N/A", "N/A", "194,000 views", "N/A"],
                ],
            }),
            results_note="Các bài viral: 194K · 150K · 136K · 82,7K · 72,8K lượt xem. "
                          "Tăng trưởng đều đặn hàng tháng từ chiến lược nội dung, không phải quảng cáo trả phí.",
            results_note_en="Viral posts: 194K · 150K · 136K · 82.7K · 72.8K views. "
                             "Steady month-on-month growth came from content strategy, not paid advertising.",
            order=6
        )
        cs6.images = [
            CaseStudyImage(image_url="babe-ig-proof/proof-1.jpg",
                            caption="Ví dụ content storytelling thực tế trên kênh: góc nhìn thẳng thắn về tiền bạc và sự nghiệp, lượt xem từ 7.444 đến 421K",
                            caption_en="Real storytelling content examples: direct takes on money and career, views from 7,444 to 421K", order=1),
            CaseStudyImage(image_url="babe-ig-proof/proof-2.jpg",
                            caption="Thêm ví dụ content storytelling trên kênh: lượt xem từ 1.999 đến 343K mỗi bài",
                            caption_en="More storytelling content examples: views from 1,999 to 343K per post", order=2),
            CaseStudyImage(image_url="babe-ig-proof/proof-3.png",
                            caption="Số liệu Instagram thật, tháng 8/2025: 477,9K views, 104,4K reach, 14,6K tương tác",
                            caption_en="Real Instagram data, August 2025: 477.9K views, 104.4K reach, 14.6K interactions", order=3),
            CaseStudyImage(image_url="babe-ig-proof/proof-4.png",
                            caption="Số liệu Instagram thật, tháng 9/2025: 786,1K views (+64,5%), 145,3K reach (+39,3%), 21,2K tương tác (+45,3%)",
                            caption_en="Real Instagram data, September 2025: 786.1K views (+64.5%), 145.3K reach (+39.3%), 21.2K interactions (+45.3%)", order=4),
        ]

        db.session.add_all([cs1, cs2, cs3, cs4, cs5, cs6])

        # ---------- Other Projects ----------
        other = [
            ("The Aura", "TikTok affiliate và huy động creator: 12 triệu lượt xem hashtag tháng đầu, 1.800 video được sản xuất, Shopee tăng trưởng 514,87%.",
             "TikTok affiliate and creator mobilization: 12M hashtag views in month one, 1,800 videos produced, 514.87% Shopee growth."),
            ("VNCreatorpreneur", "Brand awareness và affiliate: email list tăng từ 236 lên 1.012 đăng ký trong 3 tháng (+172,78% tháng 3).",
             "Brand awareness and affiliate: email list grew from 236 to 1,012 sign-ups in 3 months (+172.78% in month 3)."),
            ("Levents", "TikTok content strategy: phát triển concept chuyên sâu, storyboard chi tiết với dialogue và narrative flow, direction talent để đảm bảo output video nhất quán với brand. Video đạt 1,7M, 2,5M và 1,1M lượt xem.",
             "TikTok content strategy: in-depth concept development, detailed storyboards with dialogue and narrative flow, talent direction for brand-consistent video output. Videos reached 1.7M, 2.5M, and 1.1M views."),
            ("LOEWY", "Quản lý mạng xã hội hàng tháng và KOL/KOC, gắn với mục tiêu doanh thu 300 triệu VNĐ/tháng, tăng trưởng reach +20% trong 3 tháng.",
             "Monthly social media management and KOL/KOC, tied to a 300M VND/month revenue target, +20% reach growth in 3 months."),
            ("ResetMe", "Xây dựng thương hiệu từ số 0: nhận diện thương hiệu, content arc tiền khai trương, vận hành sau ra mắt.",
             "Built the brand from zero: brand identity, pre-launch content arc, post-launch operations."),
            ("Lanci Cosmetic", "Cộng đồng Facebook đạt 4.500 thành viên trong 3 tháng; nội dung beauty review thúc đẩy nhận diện organic.",
             "Facebook community reached 4,500 members in 3 months; beauty review content drove organic awareness."),
            ("Cháo Vịt Liên", "Chiến dịch ra mắt F&B: seeding KOL/fanpage, concept video. Doanh thu tháng đầu khoảng 100 triệu VNĐ, 100% đánh giá 5 sao Google Maps.",
             "F&B launch campaign: KOL/fanpage seeding, video concepts. About 100M VND revenue in month one, 100% 5-star Google Maps reviews."),
            ("Solitude Brand", "Quản lý mạng xã hội thương hiệu thời trang local: nhận diện thẩm mỹ riêng biệt, chọn KOL theo giá trị brand.",
             "Local fashion brand social management: distinct aesthetic identity, KOL selection based on brand values."),
            ("ODY Diamond", "Trang sức cao cấp: quản lý fanpage, chiến dịch ra mắt sản phẩm, seeding KOL/KOC đa nền tảng.",
             "Premium jewelry: fanpage management, product launch campaigns, multi-platform KOL/KOC seeding."),
            ("Allure Coffee", "Quản lý mạng xã hội F&B: nội dung lifestyle thẩm mỹ, ảnh theo mùa, tập trung thúc đẩy lượng khách đến cửa hàng.",
             "F&B social management: lifestyle aesthetic content, seasonal photography, focused on driving foot traffic."),
            ("Trạm Sheet", "Xây dựng thương hiệu sản phẩm số từ số 0: tên thương hiệu, nhận diện, hệ thống nội dung, copy, landing page, ra mắt kênh.",
             "Built a digital product brand from zero: name, identity, content system, copy, landing page, channel launch."),
            ("Zkar Auto", "Phụ kiện ô tô: tái định hướng thương hiệu, chiến lược nội dung, quản lý kênh.",
             "Automotive accessories: brand repositioning, content strategy, channel management."),
            ("Embe's Corner", "Sản phẩm hữu cơ: thâm nhập thị trường Úc qua storytelling văn hóa nhắm vào cộng đồng người Việt ở nước ngoài.",
             "Organic products: entered the Australian market through cultural storytelling aimed at the Vietnamese diaspora."),
        ]
        for i, (n, d, d_en) in enumerate(other):
            db.session.add(OtherProject(name=n, description=d, description_en=d_en, order=i))

        # ---------- How We Work ----------
        steps = [
            ("01", "Tìm hiểu về brand và mục tiêu", "Brand & Goals Discovery",
             "Brief về sản phẩm, khách hàng mục tiêu và kết quả mong muốn.",
             "A brief covering the product, target customer, and desired outcomes."),
            ("02", "Nghiên cứu đối thủ và insight khách hàng mục tiêu", "Competitor Research & Customer Insight",
             "Audit kênh, phân tích đối thủ, xác định content gap và insight.",
             "Channel audit, competitor analysis, identifying content gaps and insight."),
            ("03", "Lên chiến lược marketing tối thiểu 3 tháng", "3-Month Marketing Strategy",
             "Concept, content calendar, các hoạt động và chiến dịch chính theo tháng.",
             "Concept, content calendar, key activities and campaigns by month."),
            ("04", "Triển khai", "Execution",
             "Sản xuất nội dung, điều phối KOL/KOC, quản lý cộng đồng, chạy chiến dịch.",
             "Content production, KOL/KOC coordination, community management, campaign rollout."),
            ("05", "Báo cáo và tối ưu theo tháng", "Monthly Reporting & Optimization",
             "Số liệu thực từ platform, phân tích và điều chỉnh cho tháng tiếp theo.",
             "Real platform data, analysis, and adjustments for the next cycle."),
        ]
        for i, (num, t, t_en, d, d_en) in enumerate(steps):
            db.session.add(WorkStep(number=num, title=t, title_en=t_en, description=d, description_en=d_en, order=i))

        # ---------- Why Us ----------
        why = [
            ("Chúng tôi show tư duy, không chỉ kết quả", "We show the thinking, not just the output",
             "Mọi dự án trong portfolio này đều thể hiện chúng tôi đã làm gì và lý do tại sao. "
             "Kết quả không có chiến lược thì không thể áp dụng lại cho doanh nghiệp của bạn.",
             "Every project in this portfolio shows what we did and why. "
             "Results without strategy cannot be repeated for your business."),
            ("Small team. Direct access. Real accountability.", "Small team. Direct access. Real accountability.",
             "Bạn làm việc trực tiếp với người thực thi, không qua account manager trung gian. "
             "Quyết định nhanh hơn, giao tiếp rõ ràng hơn, brief không bị tam sao thất bản.",
             "You work directly with the people doing the work, with no account manager in between. "
             "Faster decisions, clearer communication, and briefs that never get lost in translation."),
            ("Multi-market. Multi-language. Already proven.", "Multi-market. Multi-language. Already proven.",
             "Chúng tôi đã chạy chiến dịch bằng tiếng Anh, tiếng Đức và tiếng Pháp, đồng thời tại Mỹ, Anh, Đức, Pháp và Úc. "
             "Không phải lý thuyết. Chúng tôi có con số chứng minh.",
             "We've run campaigns in English, German, and French, simultaneously across the US, UK, Germany, France, and Australia. "
             "Not theoretical. We have the numbers to prove it."),
            ("Built for SMEs who are ready to grow", "Built for SMEs who are ready to grow",
             "Chúng tôi làm tốt nhất với các thương hiệu vừa và nhỏ đang sẵn sàng tăng trưởng. "
             "Không có retainer cồng kềnh. Không có template áp dụng đại trà.",
             "We work best with small and mid-sized brands that are ready to grow. "
             "No bloated retainers. No one-size-fits-all templates."),
        ]
        for i, (t, t_en, d, d_en) in enumerate(why):
            db.session.add(WhyReason(title=t, title_en=t_en, description=d, description_en=d_en, order=i))

        # ---------- Skills ----------
        skills = [
            ("Platforms", "Platforms", "TikTok · Instagram · Facebook · YouTube Shorts · Threads · TikTok Shop",
             "TikTok · Instagram · Facebook · YouTube Shorts · Threads · TikTok Shop"),
            ("Markets", "Markets", "Việt Nam · Mỹ · Anh · Đức · Pháp · Úc",
             "Vietnam · US · UK · Germany · France · Australia"),
            ("Capabilities", "Capabilities",
             "Affiliate Marketing · KOL/KOC Management · Seasonal Campaigns · Community Building · Brand Launch · Personal Branding · Content Strategy · Brand Repositioning",
             "Affiliate Marketing · KOL/KOC Management · Seasonal Campaigns · Community Building · Brand Launch · Personal Branding · Content Strategy · Brand Repositioning"),
        ]
        for i, (l, l_en, items, items_en) in enumerate(skills):
            db.session.add(SkillGroup(label=l, label_en=l_en, items=items, items_en=items_en, order=i))

        # ---------- Site settings ----------
        db.session.add_all([
            SiteSetting(
                key="about_text",
                value="Aura Bloom là team marketing mạng xã hội dành cho các SMEs và startups cần nhiều hơn là quản lý nội dung. "
                      "Chúng tôi phát triển concept, tái định vị thương hiệu và xây dựng chiến dịch tập trung vào chuyển đổi doanh số, "
                      "không chỉ tăng nhận diện. Với kinh nghiệm thực chiến tại Việt Nam, Mỹ, Anh, Đức, Pháp và Úc, "
                      "chúng tôi đã tạo ra kết quả doanh thu thực tế cho các thương hiệu ở mọi giai đoạn phát triển.",
                value_en="Aura Bloom is a social media marketing team for SMEs and startups that need more than managed content. "
                         "We develop concepts, reposition brands, and build campaigns focused on sales conversion, not just visibility. "
                         "With hands-on experience across Vietnam, the US, UK, Germany, France, and Australia, "
                         "we've delivered measurable revenue results for brands at every stage of growth."
            ),
            SiteSetting(
                key="why_sub",
                value="Chúng tôi không quản lý nội dung. Chúng tôi xây hệ thống giúp thương hiệu tăng trưởng doanh thu.",
                value_en="We don't manage content. We build systems that grow revenue."
            ),
            SiteSetting(key="contact_email", value="aurabloom.forwork@gmail.com", value_en="aurabloom.forwork@gmail.com"),
            SiteSetting(key="contact_whatsapp", value="+84 365 334 549", value_en="+84 365 334 549"),
            SiteSetting(
                key="closing_line",
                value="Chúng tôi không chỉ quản lý mạng xã hội. Chúng tôi xây hệ thống giúp thương hiệu tăng trưởng.",
                value_en="We don't just manage social media. We build the systems that make brands grow."
            ),
        ])

        db.session.commit()
        print("Seed completed.")


if __name__ == "__main__":
    run()
