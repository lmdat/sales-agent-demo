import os
from dotenv import load_dotenv, find_dotenv
from textwrap import dedent
from pinecone import Pinecone

load_dotenv(find_dotenv())

pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def company_info_data():
    data = [
        {
            'title': 'Giới thiệu công ty.',
            'content': "Suốt 10 năm qua, Miracle Life đã không ngừng nỗ lực để mang đến những sản phẩm skincare chất lượng cao, an toàn và hiệu quả, giúp hàng ngàn khách hàng tự tin tỏa sáng với làn da khỏe mạnh và rạng rỡ. Chúng tôi không chỉ đơn thuần là một công ty mỹ phẩm, mà còn là người bạn đồng hành, là chuyên gia tư vấn, luôn lắng nghe và thấu hiểu những mong muốn của bạn trên hành trình chăm sóc sắc đẹp."
        },
        {
            'title': 'Triết lý kinh doanh.',
            'content': "Chúng tôi luôn đặt chất lượng lên hàng đầu trong mọi hoạt động. Từ khâu nghiên cứu, phát triển công thức, lựa chọn nguyên liệu đến quy trình sản xuất và kiểm soát chất lượng, tất cả đều được thực hiện một cách nghiêm ngặt, tuân thủ theo các tiêu chuẩn quốc tế."
        },
        {
            'title': 'Sứ mệnh và Tầm nhìn.',
            'content': """- Sứ mệnh: Mang đến cho khách hàng những sản phẩm skincare chất lượng cao, an toàn và hiệu quả, giúp họ tự tin tỏa sáng với làn da khỏe mạnh và rạng rỡ.
            - Tầm nhìn: Trở thành thương hiệu mỹ phẩm hàng đầu Việt Nam, được khách hàng tin yêu và lựa chọn, đồng thời góp phần vào sự phát triển của ngành công nghiệp làm đẹp bền vững."""
        },
        {
            'title': 'Giá trị cốt lõi.',
            'content': """- Chất lượng: Đặt chất lượng lên hàng đầu trong mọi hoạt động.
            - Sáng tạo: Không ngừng đổi mới và sáng tạo để mang đến những sản phẩm đột phá.
            - Tận tâm: Luôn lắng nghe và thấu hiểu khách hàng, cung cấp dịch vụ tận tâm và chu đáo.
            - Uy tín: Xây dựng uy tín dựa trên sự trung thực và trách nhiệm.
            - Bền vững: Phát triển bền vững, thân thiện với môi trường."""
        },
        {
            'title': 'Thông tin liên hệ của công ty Miracle Life.',
            'content': """Công ty TNHH Miracle Life
            - Trụ sở chính: 9999 Trần Hưng Đạo, Quận 5, TPHCM
            - Email: info@miraclelife.com
            - Phone: 0123456789
            - Hotline: 0919666888"""
        }
    ]

    
    for i, item in enumerate(data):
        item['id'] = str(i + 1)
        item['chunk_content'] = f"{item['title']}\n----------\n{dedent(item['content'])}"
        
    return data

def products_data():
    data = [
        {
            "title": "Nước hoa nữ Chanel No.5 Eau de Parfum",
            "category": "perfume",
            "category_name": "Nước hoa",
            "sku": "NUOC-HOA-CN-001",
            "price": 1200000,
            "description": "Chanel No.5 Eau de Parfum là một biểu tượng vượt thời gian trong thế giới nước hoa. Được tạo ra bởi Gabrielle Chanel, hương thơm này mang đến sự quyến rũ, sang trọng và đẳng cấp. Mở đầu với hương aldehyde tươi mát, kết hợp cùng hoa nhài và hoa hồng Grasse, tạo nên một lớp hương hoa cỏ nồng nàn và quyến rũ. Lớp hương cuối là sự hòa quyện của gỗ đàn hương, vani và hổ phách, mang đến sự ấm áp và lưu hương lâu dài. Chanel No.5 là sự lựa chọn hoàn hảo cho những người phụ nữ tự tin, thanh lịch và yêu thích sự cổ điển.",
            "url": "https://example.com/nuoc-hoa-chanel-no5.html"
        },
        {
            "title": "Nước hoa nam Dior Sauvage Eau de Toilette",
            "category": "perfume",
            "category_name": "Nước hoa",
            "sku": "NUOC-HOA-DIOR-002",
            "price": 1100000,
            "description": "Dior Sauvage Eau de Toilette là một hương thơm nam tính mạnh mẽ và đầy lôi cuốn. Được lấy cảm hứng từ thiên nhiên hoang dã, Sauvage mang đến sự tươi mát của cam Bergamot Calabria, hòa quyện cùng hương Ambroxan và gỗ tuyết tùng. Hương thơm này tạo nên một sự tương phản độc đáo giữa sự tươi mát và sự ấm áp, phù hợp với những người đàn ông mạnh mẽ, tự do và yêu thích khám phá. Sauvage là một lựa chọn hoàn hảo cho cả ngày lẫn đêm, mang đến sự tự tin và quyến rũ.",
            "url": "https://example.com/nuoc-hoa-dior-sauvage.html"
        },
        {
            "title": "Nước hoa unisex Le Labo Santal 33 Eau de Parfum",
            "category": "perfume",
            "category_name": "Nước hoa",
            "sku": "NUOC-HOA-LL-003",
            "price": 2500000,
            "description": "Le Labo Santal 33 Eau de Parfum là một hương thơm unisex độc đáo và cá tính. Với hương gỗ đàn hương làm chủ đạo, Santal 33 mang đến sự ấm áp, bí ẩn và gợi cảm. Hương thơm này còn được kết hợp với các nốt hương khác như da thuộc, giấy cói và hoa violet, tạo nên một sự pha trộn phức tạp và cuốn hút. Santal 33 phù hợp với những người yêu thích sự khác biệt, muốn thể hiện cá tính riêng và không ngại thử thách.",
            "url": "https://example.com/nuoc-hoa-le-labo-santal33.html"
        },
        {
            "title": "Nước hoa nữ Lancôme La Vie Est Belle Eau de Parfum",
            "category": "perfume",
            "category_name": "Nước hoa",
            "sku": "NUOC-HOA-LC-004",
            "price": 1000000,
            "description": "Lancôme La Vie Est Belle Eau de Parfum là một hương thơm ngọt ngào và nữ tính, mang đến niềm vui và hạnh phúc. Hương thơm này mở đầu với hương quả lý chua đen và quả lê, tiếp theo là hương hoa diên vĩ, hoa nhài và hoa cam. Lớp hương cuối là sự hòa quyện của hoắc hương, đậu tonka, vani và kẹo hạnh nhân, tạo nên một sự ngọt ngào và ấm áp. La Vie Est Belle là sự lựa chọn hoàn hảo cho những người phụ nữ yêu đời, lạc quan và luôn tìm kiếm những điều tốt đẹp trong cuộc sống.",
            "url": "https://example.com/nuoc-hoa-lancome-la-vie-est-belle.html"
        },
        {
            "title": "Nước hoa nam Creed Aventus Eau de Parfum",
            "category": "perfume",
            "category_name": "Nước hoa",
            "sku": "NUOC-HOA-CR-005",
            "price": 6000000,
            "description": "Creed Aventus Eau de Parfum là một hương thơm nam tính mạnh mẽ và đầy quyền lực. Được lấy cảm hứng từ cuộc đời của Napoleon Bonaparte, Aventus mang đến sự tự tin, thành công và sự quyến rũ. Hương thơm này mở đầu với hương dứa, cam Bergamot, táo và quả lý chua đen, tiếp theo là hương hoa hồng, hoa nhài và hoắc hương. Lớp hương cuối là sự hòa quyện của hổ phách, vani, rêu sồi và xạ hương, tạo nên một sự ấm áp, nam tính và lưu hương lâu dài. Aventus là sự lựa chọn hoàn hảo cho những người đàn ông thành đạt, tự tin và muốn khẳng định vị thế của mình.",
            "url": "https://example.com/nuoc-hoa-creed-aventus.html"
        },
        {
            "title": "Nước hoa unisex Byredo Gypsy Water Eau de Parfum",
            "category": "perfume",
            "category_name": "Nước hoa",
            "sku": "NUOC-HOA-BY-006",
            "price": 5000000,
            "description": "Byredo Gypsy Water Eau de Parfum là một hương thơm unisex phóng khoáng và tự do, mang đến cảm giác phiêu lưu và khám phá. Hương thơm này mở đầu với hương cam Bergamot, chanh và tiêu, tiếp theo là hương nhũ hương, cây thông và rễ cây orris. Lớp hương cuối là sự hòa quyện của hổ phách, vani và gỗ đàn hương, tạo nên một sự ấm áp, bí ẩn và lưu hương lâu dài. Gypsy Water là sự lựa chọn hoàn hảo cho những người yêu thích du lịch, khám phá những vùng đất mới và muốn thể hiện sự tự do trong tâm hồn.",
            "url": "https://example.com/nuoc-hoa-byredo-gypsy-water.html"
        },
        {
            "title": "Sữa tắm dưỡng ẩm Dove Deep Moisture Body Wash",
            "category": "shower-gel",
            "category_name": "Sữa tắm",
            "sku": "SUA-TAM-DV-001",
            "price": 80000,
            "description": "Sữa tắm Dove Deep Moisture Body Wash là một sản phẩm chăm sóc da hàng ngày lý tưởng để giúp bạn có một làn da mềm mại, mịn màng và khỏe mạnh. Với công thức chứa NutriumMoisture™, sữa tắm này cung cấp dưỡng chất sâu vào da, giúp phục hồi độ ẩm tự nhiên và ngăn ngừa tình trạng khô da. Hương thơm dịu nhẹ của Dove sẽ mang đến cho bạn cảm giác thư giãn và sảng khoái sau mỗi lần tắm. Sản phẩm phù hợp với mọi loại da, đặc biệt là da khô và nhạy cảm. Hãy trải nghiệm sự khác biệt mà Dove Deep Moisture Body Wash mang lại!",
            "url": "https://example.com/sua-tam-dove-deep-moisture.html"
        },
        {
            "title": "Sữa tắm trắng da Purité de Prôvence Cherry Blossom Shower Cream",
            "category": "shower-gel",
            "category_name": "Sữa tắm",
            "sku": "SUA-TAM-PP-002",
            "price": 120000,
            "description": "Sữa tắm Purité de Prôvence Cherry Blossom Shower Cream là sự kết hợp hoàn hảo giữa hương thơm hoa anh đào quyến rũ và khả năng dưỡng trắng da hiệu quả. Sản phẩm chứa chiết xuất hoa anh đào giàu vitamin và chất chống oxy hóa, giúp làm sáng da, cải thiện tông màu da và bảo vệ da khỏi tác hại của môi trường. Sữa tắm còn chứa các thành phần dưỡng ẩm giúp da mềm mại, mịn màng và không bị khô căng sau khi tắm. Hãy đắm mình trong hương thơm ngọt ngào của hoa anh đào và cảm nhận làn da trắng sáng rạng rỡ!",
            "url": "https://example.com/sua-tam-purite-cherry-blossom.html"
        },
        {
            "title": "Sữa tắm kháng khuẩn Lifebuoy Total 10 Body Wash",
            "category": "shower-gel",
            "category_name": "Sữa tắm",
            "sku": "SUA-TAM-LB-003",
            "price": 70000,
            "description": "Sữa tắm Lifebuoy Total 10 Body Wash là giải pháp bảo vệ da khỏi vi khuẩn hàng ngày hiệu quả. Với công thức chứa Activ Silver+, sữa tắm này giúp loại bỏ 99.9% vi khuẩn gây bệnh, bảo vệ bạn và gia đình khỏi các bệnh nhiễm trùng da. Sản phẩm có hương thơm tươi mát, mang đến cảm giác sảng khoái và sạch sẽ sau khi tắm. Lifebuoy Total 10 Body Wash là sự lựa chọn lý tưởng cho những người quan tâm đến sức khỏe và vệ sinh cá nhân.",
            "url": "https://example.com/sua-tam-lifebuoy-total10.html"
        },
        {
            "title": "Sữa tắm cho bé Cetaphil Baby Gentle Wash & Shampoo",
            "category": "shower-gel",
            "category_name": "Sữa tắm",
            "sku": "SUA-TAM-CT-004",
            "price": 250000,
            "description": "Sữa tắm Cetaphil Baby Gentle Wash & Shampoo là sản phẩm dịu nhẹ được thiết kế đặc biệt cho làn da nhạy cảm của bé. Với công thức không chứa xà phòng, không gây kích ứng và đã được kiểm nghiệm da liễu, sữa tắm này nhẹ nhàng làm sạch da và tóc của bé, đồng thời cung cấp độ ẩm cần thiết để da luôn mềm mại và mịn màng. Cetaphil Baby Gentle Wash & Shampoo có thể sử dụng hàng ngày cho bé từ sơ sinh. Hãy yên tâm chăm sóc làn da của bé yêu với Cetaphil!",
            "url": "https://example.com/sua-tam-cetaphil-baby.html"
        },
        {
            "title": "Sữa tắm giảm mụn lưng Cocoon Winter Melon Body Wash",
            "category": "shower-gel",
            "category_name": "Sữa tắm",
            "sku": "SUA-TAM-CC-005",
            "price": 180000,
            "description": "Sữa tắm Cocoon Winter Melon Body Wash là sản phẩm đặc trị mụn lưng hiệu quả với thành phần chính là bí đao. Bí đao có tác dụng kháng viêm, giảm sưng và làm dịu da, giúp giảm thiểu tình trạng mụn lưng và ngăn ngừa mụn tái phát. Sữa tắm còn chứa AHA và BHA giúp loại bỏ tế bào chết, làm thông thoáng lỗ chân lông và cải thiện tông màu da. Sản phẩm có hương thơm thảo mộc tự nhiên, mang đến cảm giác thư giãn và dễ chịu. Hãy tạm biệt nỗi lo mụn lưng với Cocoon Winter Melon Body Wash!",
            "url": "https://example.com/sua-tam-cocoon-winter-melon.html"
        },
        {
            "title": "Sữa tắm hương nước hoa Tesori d'Oriente White Musk Shower Cream",
            "category": "shower-gel",
            "category_name": "Sữa tắm",
            "sku": "SUA-TAM-TD-006",
            "price": 150000,
            "description": "Sữa tắm Tesori d'Oriente White Musk Shower Cream là sự kết hợp hoàn hảo giữa khả năng làm sạch dịu nhẹ và hương thơm nước hoa quyến rũ. Sữa tắm chứa tinh chất xạ hương trắng quý hiếm, mang đến hương thơm ấm áp, gợi cảm và lưu hương lâu dài trên da. Sản phẩm còn chứa các thành phần dưỡng ẩm giúp da mềm mại, mịn màng và không bị khô căng sau khi tắm. Hãy tận hưởng cảm giác thư giãn như đang ở spa với Tesori d'Oriente White Musk Shower Cream!",
            "url": "https://example.com/sua-tam-tesori-white-musk.html"
        },
        {
            "title": "Tinh dầu xông phòng sả chanh nguyên chất Kodo",
            "category": "essential-oil",
            "category_name": "Tinh dầu xông",
            "sku": "TINH-DAU-KD-001",
            "price": 100000,
            "description": "Tinh dầu sả chanh Kodo là sản phẩm 100% nguyên chất, được chiết xuất từ lá và thân cây sả chanh tươi. Với hương thơm tươi mát, dễ chịu, tinh dầu sả chanh có nhiều công dụng tuyệt vời: giúp khử mùi, thanh lọc không khí, xua đuổi côn trùng, giảm căng thẳng, mệt mỏi và tăng cường khả năng tập trung. Bạn có thể sử dụng tinh dầu sả chanh để xông phòng, xông hơi, massage hoặc pha vào nước tắm. Hãy tạo không gian sống trong lành và thư giãn với tinh dầu sả chanh Kodo!",
            "url": "https://example.com/tinh-dau-xa-chanh-kodo.html"
        },
        {
            "title": "Tinh dầu xông phòng oải hương nguyên chất Soapberry",
            "category": "essential-oil",
            "category_name": "Tinh dầu xông",
            "sku": "TINH-DAU-SB-002",
            "price": 120000,
            "description": "Tinh dầu oải hương Soapberry là sản phẩm 100% nguyên chất, được chiết xuất từ hoa oải hương tươi. Với hương thơm dịu nhẹ, thư giãn, tinh dầu oải hương có nhiều công dụng tuyệt vời: giúp giảm căng thẳng, lo âu, cải thiện giấc ngủ, giảm đau đầu và kháng viêm. Bạn có thể sử dụng tinh dầu oải hương để xông phòng, xông hơi, massage hoặc pha vào nước tắm. Hãy tận hưởng giấc ngủ ngon và sâu giấc với tinh dầu oải hương Soapberry!",
            "url": "https://example.com/tinh-dau-oai-huong-soapberry.html"
        },
        {
            "title": "Tinh dầu xông phòng bạc hà nguyên chất Green Garden",
            "category": "essential-oil",
            "category_name": "Tinh dầu xông",
            "sku": "TINH-DAU-GG-003",
            "price": 80000,
            "description": "Tinh dầu bạc hà Green Garden là sản phẩm 100% nguyên chất, được chiết xuất từ lá bạc hà tươi. Với hương thơm the mát, sảng khoái, tinh dầu bạc hà có nhiều công dụng tuyệt vời: giúp thông mũi, giảm nghẹt thở, giảm đau đầu, tăng cường sự tỉnh táo và tập trung. Bạn có thể sử dụng tinh dầu bạc hà để xông phòng, xông hơi, massage hoặc pha vào nước tắm. Hãy cảm nhận sự tỉnh táo và sảng khoái với tinh dầu bạc hà Green Garden!",
            "url": "https://example.com/tinh-dau-bac-ha-green-garden.html"
        },
        {
            "title": "Tinh dầu xông phòng tràm trà nguyên chất Organic Care",
            "category": "essential-oil",
            "category_name": "Tinh dầu xông",
            "sku": "TINH-DAU-OC-004",
            "price": 150000,
            "description": "Tinh dầu tràm trà Organic Care là sản phẩm 100% nguyên chất, được chiết xuất từ lá cây tràm trà. Với hương thơm đặc trưng, hơi cay nồng, tinh dầu tràm trà có nhiều công dụng tuyệt vời: kháng khuẩn, kháng viêm, trị mụn, giảm ngứa do côn trùng cắn và hỗ trợ điều trị các bệnh về da. Bạn có thể sử dụng tinh dầu tràm trà để xông phòng, xông hơi, massage hoặc thoa trực tiếp lên vùng da bị mụn. Hãy bảo vệ làn da khỏe mạnh với tinh dầu tràm trà Organic Care!",
            "url": "https://example.com/tinh-dau-tram-tra-organic-care.html"
        },
        {
            "title": "Tinh dầu xông phòng cam ngọt nguyên chất Eco Aroma",
            "category": "essential-oil",
            "category_name": "Tinh dầu xông",
            "sku": "TINH-DAU-EA-005",
            "price": 110000,
            "description": "Tinh dầu cam ngọt Eco Aroma là sản phẩm 100% nguyên chất, được chiết xuất từ vỏ cam tươi. Với hương thơm ngọt ngào, tươi vui, tinh dầu cam ngọt có nhiều công dụng tuyệt vời: giúp giảm căng thẳng, cải thiện tâm trạng, tăng cường hệ miễn dịch và khử mùi hiệu quả. Bạn có thể sử dụng tinh dầu cam ngọt để xông phòng, xông hơi, massage hoặc pha vào nước tắm. Hãy tạo không gian sống ấm áp và tràn đầy năng lượng với tinh dầu cam ngọt Eco Aroma!",
            "url": "https://example.com/tinh-dau-cam-ngot-eco-aroma.html"
        },
        {
            "title": "Tinh dầu xông phòng hoa hồng nguyên chất Rose Essential",
            "category": "essential-oil",
            "category_name": "Tinh dầu xông",
            "sku": "TINH-DAU-RE-006",
            "price": 200000,
            "description": "Tinh dầu hoa hồng Rose Essential là sản phẩm 100% nguyên chất, được chiết xuất từ cánh hoa hồng tươi. Với hương thơm nồng nàn, quyến rũ, tinh dầu hoa hồng có nhiều công dụng tuyệt vời: giúp giảm căng thẳng, cải thiện tâm trạng, làm đẹp da, tăng cường sự tự tin và lãng mạn. Bạn có thể sử dụng tinh dầu hoa hồng để xông phòng, xông hơi, massage hoặc pha vào nước tắm. Hãy tận hưởng sự sang trọng và quý phái với tinh dầu hoa hồng Rose Essential!",
            "url": "https://example.com/tinh-dau-hoa-hong-rose-essential.html"
        },
        {
            "title": "Dầu gội đầu Pantene Pro-V ngăn rụng tóc",
            "category": "shampoo",
            "category_name": "Dầu gội đầu",
            "sku": "DAU-GOI-PT-001",
            "price": 90000,
            "description": "Dầu gội Pantene Pro-V ngăn rụng tóc là giải pháp hiệu quả cho mái tóc yếu và dễ gãy rụng. Với công thức Pro-V độc đáo, sản phẩm cung cấp dưỡng chất sâu vào chân tóc, giúp tăng cường độ chắc khỏe, giảm thiểu tình trạng rụng tóc và kích thích mọc tóc mới. Dầu gội còn chứa các thành phần dưỡng ẩm giúp tóc mềm mượt, óng ả và dễ chải. Hãy sở hữu mái tóc khỏe mạnh, dày dặn và tràn đầy sức sống với Pantene Pro-V ngăn rụng tóc!",
            "url": "https://example.com/dau-goi-pantene-ngan-rung-toc.html"
        },
        {
            "title": "Dầu gội đầu TRESemmé Keratin Smooth cho tóc suôn mượt",
            "category": "shampoo",
            "category_name": "Dầu gội đầu",
            "sku": "DAU-GOI-TR-002",
            "price": 120000,
            "description": "Dầu gội TRESemmé Keratin Smooth là lựa chọn lý tưởng cho những ai mong muốn có mái tóc suôn mượt, vào nếp và không bị xơ rối. Với công thức chứa keratin và dầu Marula, sản phẩm giúp phục hồi cấu trúc tóc, làm mềm mượt tóc và giảm thiểu tình trạng tóc xoăn cứng, khó vào nếp. Dầu gội còn giúp bảo vệ tóc khỏi nhiệt độ cao khi tạo kiểu. Hãy tự tin tỏa sáng với mái tóc suôn mượt, óng ả như ở salon với TRESemmé Keratin Smooth!",
            "url": "https://example.com/dau-goi-tresemme-keratin-smooth.html"
        },
        {
            "title": "Dầu gội đầu Clear Men Cool Sport bạc hà mát lạnh",
            "category": "shampoo",
            "category_name": "Dầu gội đầu",
            "sku": "DAU-GOI-CM-003",
            "price": 80000,
            "description": "Dầu gội Clear Men Cool Sport bạc hà mát lạnh là sản phẩm dành riêng cho nam giới, giúp làm sạch sâu da đầu, loại bỏ gàu và mang đến cảm giác sảng khoái, mát lạnh. Với công thức chứa tinh chất bạc hà, sản phẩm giúp làm dịu da đầu, giảm ngứa và ngăn ngừa gàu tái phát. Dầu gội còn chứa các thành phần dưỡng chất giúp tóc khỏe mạnh, chắc khỏe và bóng mượt. Hãy tự tin với mái tóc sạch gàu và cảm giác mát lạnh sảng khoái với Clear Men Cool Sport!",
            "url": "https://example.com/dau-goi-clear-men-cool-sport.html"
        },
        {
            "title": "Dầu gội đầu Nguyên Xuân bồng bềnh dược liệu",
            "category": "shampoo",
            "category_name": "Dầu gội đầu",
            "sku": "DAU-GOI-NX-004",
            "price": 150000,
            "description": "Dầu gội Nguyên Xuân bồng bềnh dược liệu là sản phẩm chăm sóc tóc được chiết xuất từ các loại thảo dược thiên nhiên như bồ kết, cỏ mần trầu, hương nhu, hà thủ ô... Sản phẩm giúp làm sạch tóc và da đầu một cách nhẹ nhàng, cung cấp dưỡng chất giúp tóc khỏe mạnh, giảm gãy rụng và kích thích mọc tóc. Dầu gội còn giúp cân bằng độ ẩm cho da đầu, ngăn ngừa gàu và mang đến mái tóc bồng bềnh, óng ả. Hãy trải nghiệm sự khác biệt từ thảo dược thiên nhiên với dầu gội Nguyên Xuân!",
            "url": "https://example.com/dau-goi-nguyen-xuan-bong-benh.html"
        },
        {
            "title": "Dầu gội đầu Sunsilk mềm mượt diệu kỳ",
            "category": "shampoo",
            "category_name": "Dầu gội đầu",
            "sku": "DAU-GOI-SL-005",
            "price": 70000,
            "description": "Dầu gội Sunsilk mềm mượt diệu kỳ là sản phẩm giúp bạn có mái tóc mềm mượt, óng ả và dễ chải. Với công thức Nutri-Silk™ độc đáo, sản phẩm cung cấp dưỡng chất giúp tóc mềm mại từ gốc đến ngọn, giảm thiểu tình trạng tóc xơ rối, khó chải và dễ gãy rụng. Dầu gội còn có hương thơm quyến rũ, lưu hương lâu dài trên tóc. Hãy sở hữu mái tóc mềm mượt như nhung với Sunsilk mềm mượt diệu kỳ!",
            "url": "https://example.com/dau-goi-sunsilk-mem-muot.html"
        },
        {
            "title": "Dầu gội đầu Biotin & Collagen OGX dày mượt tóc",
            "category": "shampoo",
            "category_name": "Dầu gội đầu",
            "sku": "DAU-GOI-BC-006",
            "price": 250000,
            "description": "Dầu gội Biotin & Collagen OGX là sản phẩm giúp bạn có mái tóc dày dặn, bồng bềnh và khỏe mạnh. Với công thức chứa biotin và collagen, sản phẩm giúp tăng cường độ đàn hồi của tóc, giảm gãy rụng và kích thích mọc tóc mới. Dầu gội còn cung cấp dưỡng chất giúp tóc bóng mượt, óng ả và đầy sức sống. Hãy sở hữu mái tóc dày mượt như mơ ước với Biotin & Collagen OGX!",
            "url": "https://example.com/dau-goi-biotin-collagen-ogx.html"
        },
        {
            "title": "Xà phòng thiên nhiên handmade trà xanh",
            "category": "natural-soap",
            "category_name": "Xà phòng thiên nhiên",
            "sku": "XA-PHONG-TX-001",
            "price": 50000,
            "description": "Xà phòng handmade trà xanh là sản phẩm hoàn toàn tự nhiên, được làm thủ công từ dầu thực vật và chiết xuất trà xanh. Trà xanh có tác dụng chống oxy hóa, kháng viêm, làm sạch da và giúp da sáng mịn. Xà phòng còn chứa các thành phần dưỡng ẩm giúp da mềm mại, không bị khô căng sau khi sử dụng. Sản phẩm phù hợp với mọi loại da, đặc biệt là da dầu và da mụn. Hãy trải nghiệm sự khác biệt từ xà phòng thiên nhiên handmade!",
            "url": "https://example.com/xa-phong-tra-xanh-handmade.html"
        },
        {
            "title": "Xà phòng thiên nhiên handmade than hoạt tính",
            "category": "natural-soap",
            "category_name": "Xà phòng thiên nhiên",
            "sku": "XA-PHONG-TH-002",
            "price": 60000,
            "description": "Xà phòng handmade than hoạt tính là sản phẩm hoàn toàn tự nhiên, được làm thủ công từ dầu thực vật và than hoạt tính. Than hoạt tính có tác dụng hút sạch bụi bẩn, dầu thừa và độc tố trên da, giúp làm sạch sâu lỗ chân lông và ngăn ngừa mụn. Xà phòng còn chứa các thành phần dưỡng ẩm giúp da mềm mại, không bị khô căng sau khi sử dụng. Sản phẩm phù hợp với da dầu, da mụn và da có lỗ chân lông to. Hãy làm sạch sâu và thanh lọc làn da với xà phòng than hoạt tính handmade!",
            "url": "https://example.com/xa-phong-than-hoat-tinh-handmade.html"
        },
        {
            "title": "Xà phòng thiên nhiên handmade hoa cúc",
            "category": "natural-soap",
            "category_name": "Xà phòng thiên nhiên",
            "sku": "XA-PHONG-HC-003",
            "price": 55000,
            "description": "Xà phòng handmade hoa cúc là sản phẩm hoàn toàn tự nhiên, được làm thủ công từ dầu thực vật và chiết xuất hoa cúc. Hoa cúc có tác dụng làm dịu da, giảm kích ứng, kháng viêm và giúp da sáng mịn. Xà phòng còn chứa các thành phần dưỡng ẩm giúp da mềm mại, không bị khô căng sau khi sử dụng. Sản phẩm phù hợp với da nhạy cảm, da khô và da dễ bị kích ứng. Hãy chăm sóc làn da dịu nhẹ với xà phòng hoa cúc handmade!",
            "url": "https://example.com/xa-phong-hoa-cuc-handmade.html"
        },
        {
            "title": "Xà phòng thiên nhiên handmade mật ong",
            "category": "natural-soap",
            "category_name": "Xà phòng thiên nhiên",
            "sku": "XA-PHONG-MO-004",
            "price": 70000,
            "description": "Xà phòng handmade mật ong là sản phẩm hoàn toàn tự nhiên, được làm thủ công từ dầu thực vật và mật ong. Mật ong có tác dụng dưỡng ẩm, kháng khuẩn, làm dịu da và giúp da mềm mại, mịn màng. Xà phòng còn chứa các thành phần dưỡng ẩm giúp da không bị khô căng sau khi sử dụng. Sản phẩm phù hợp với mọi loại da, đặc biệt là da khô và da thiếu ẩm. Hãy nuôi dưỡng làn da mềm mại và khỏe mạnh với xà phòng mật ong handmade!",
            "url": "https://example.com/xa-phong-mat-ong-handmade.html"
        },
        {
            "title": "Xà phòng thiên nhiên handmade nha đam",
            "category": "natural-soap",
            "category_name": "Xà phòng thiên nhiên",
            "sku": "XA-PHONG-NA-005",
            "price": 45000,
            "description": "Xà phòng handmade nha đam là sản phẩm hoàn toàn tự nhiên, được làm thủ công từ dầu thực vật và chiết xuất nha đam. Nha đam có tác dụng làm dịu da, giảm kích ứng, dưỡng ẩm và giúp da phục hồi nhanh chóng sau tổn thương. Xà phòng còn chứa các thành phần dưỡng ẩm giúp da mềm mại, không bị khô căng sau khi sử dụng. Sản phẩm phù hợp với da cháy nắng, da bị kích ứng và da cần phục hồi. Hãy làm dịu và phục hồi làn da với xà phòng nha đam handmade!",
            "url": "https://example.com/xa-phong-nha-dam-handmade.html"
        },
        {
            "title": "Xà phòng thiên nhiên handmade cám gạo",
            "category": "natural-soap",
            "category_name": "Xà phòng thiên nhiên",
            "sku": "XA-PHONG-CG-006",
            "price": 50000,
            "description": "Xà phòng handmade cám gạo là sản phẩm hoàn toàn tự nhiên, được làm thủ công từ dầu thực vật và cám gạo. Cám gạo có tác dụng làm sáng da, tẩy tế bào chết nhẹ nhàng, giúp da mịn màng và đều màu hơn. Xà phòng còn chứa các thành phần dưỡng ẩm giúp da mềm mại, không bị khô căng sau khi sử dụng. Sản phẩm phù hợp với mọi loại da, đặc biệt là da xỉn màu và da cần làm sáng. Hãy làm sáng và mịn màng làn da với xà phòng cám gạo handmade!",
            "url": "https://example.com/xa-phong-cam-gao-handmade.html"
        },
        {
            "title": "Sữa rửa mặt Cerave Foaming Facial Cleanser",
            "category": "facial-cleanser",
            "category_name": "Sữa rửa mặt",
            "sku": "SUA-RUA-MT-CE-001",
            "price": 250000,
            "description": "Sữa rửa mặt Cerave Foaming Facial Cleanser là sản phẩm lý tưởng cho da dầu và da hỗn hợp. Với công thức chứa ceramides, hyaluronic acid và niacinamide, sản phẩm giúp làm sạch sâu da, loại bỏ bụi bẩn, dầu thừa và lớp trang điểm mà không làm khô da. Cerave Foaming Facial Cleanser giúp duy trì hàng rào bảo vệ tự nhiên của da, làm dịu da và giảm kích ứng. Sản phẩm không chứa hương liệu, không gây mụn và đã được kiểm nghiệm da liễu. Hãy làm sạch sâu và bảo vệ làn da với Cerave!",
            "url": "https://example.com/sua-rua-mat-cerave-foaming.html"
        },
        {
            "title": "Sữa rửa mặt Senka Perfect Whip",
            "category": "facial-cleanser",
            "category_name": "Sữa rửa mặt",
            "sku": "SUA-RUA-MT-SK-002",
            "price": 80000,
            "description": "Sữa rửa mặt Senka Perfect Whip là sản phẩm được yêu thích bởi khả năng tạo bọt siêu mịn, giúp làm sạch sâu da và loại bỏ bụi bẩn, dầu thừa hiệu quả. Với công thức chứa sericin và hyaluronic acid, sản phẩm giúp duy trì độ ẩm tự nhiên của da, không làm khô da sau khi rửa mặt. Senka Perfect Whip có hương thơm nhẹ nhàng, mang đến cảm giác sảng khoái sau khi sử dụng. Sản phẩm phù hợp với mọi loại da. Hãy trải nghiệm làn da sạch mịn và tươi sáng với Senka!",
            "url": "https://example.com/sua-rua-mat-senka-perfect-whip.html"
        },
        {
            "title": "Sữa rửa mặt Cosrx Low pH Good Morning Gel Cleanser",
            "category": "facial-cleanser",
            "category_name": "Sữa rửa mặt",
            "sku": "SUA-RUA-MT-CX-003",
            "price": 150000,
            "description": "Sữa rửa mặt Cosrx Low pH Good Morning Gel Cleanser là sản phẩm dịu nhẹ được thiết kế đặc biệt cho da nhạy cảm và da mụn. Với độ pH lý tưởng 5.5, sản phẩm giúp làm sạch da một cách nhẹ nhàng, không làm mất đi lớp dầu tự nhiên của da và không gây kích ứng. Cosrx Low pH Good Morning Gel Cleanser chứa BHA giúp làm sạch sâu lỗ chân lông, giảm mụn đầu đen và mụn cám. Sản phẩm còn chứa tinh dầu tràm trà giúp kháng viêm và làm dịu da. Hãy làm sạch da dịu nhẹ và bảo vệ làn da với Cosrx!",
            "url": "https://example.com/sua-rua-mat-cosrx-low-ph.html"
        },
        {
            "title": "Sữa rửa mặt Innisfree Green Tea Foam Cleanser",
            "category": "facial-cleanser",
            "category_name": "Sữa rửa mặt",
            "sku": "SUA-RUA-MT-IF-004",
            "price": 180000,
            "description": "Sữa rửa mặt Innisfree Green Tea Foam Cleanser là sản phẩm được chiết xuất từ trà xanh hữu cơ, giúp làm sạch da nhẹ nhàng, loại bỏ bụi bẩn, dầu thừa và lớp trang điểm còn sót lại. Trà xanh có tác dụng chống oxy hóa, kháng viêm và làm dịu da, giúp da sáng mịn và khỏe mạnh. Innisfree Green Tea Foam Cleanser còn chứa các thành phần dưỡng ẩm giúp da mềm mại, không bị khô căng sau khi rửa mặt. Sản phẩm phù hợp với mọi loại da, đặc biệt là da dầu và da hỗn hợp. Hãy trải nghiệm làn da tươi mát và khỏe mạnh với Innisfree!",
            "url": "https://example.com/sua-rua-mat-innisfree-green-tea.html"
        },
        {
            "title": "Sữa rửa mặt Kiehl's Ultra Facial Cleanser",
            "category": "facial-cleanser",
            "category_name": "Sữa rửa mặt",
            "sku": "SUA-RUA-MT-KL-005",
            "price": 600000,
            "description": "Sữa rửa mặt Kiehl's Ultra Facial Cleanser là sản phẩm dịu nhẹ được thiết kế cho mọi loại da, kể cả da nhạy cảm. Với công thức chứa squalane, dầu quả bơ và vitamin E, sản phẩm giúp làm sạch da một cách nhẹ nhàng, loại bỏ bụi bẩn, dầu thừa và lớp trang điểm mà không làm khô da. Kiehl's Ultra Facial Cleanser giúp duy trì độ ẩm tự nhiên của da, làm dịu da và bảo vệ da khỏi các tác nhân gây hại từ môi trường. Sản phẩm không chứa xà phòng, không paraben và không hương liệu. Hãy làm sạch da dịu nhẹ và nuôi dưỡng làn da với Kiehl's!",
            "url": "https://example.com/sua-rua-mat-kiehls-ultra-facial.html"
        },
        {
            "title": "Sữa rửa mặt La Roche-Posay Effaclar Gel Moussant Purifiant",
            "category": "facial-cleanser",
            "category_name": "Sữa rửa mặt",
            "sku": "SUA-RUA-MT-LP-006",
            "price": 350000,
            "description": "Sữa rửa mặt La Roche-Posay Effaclar Gel Moussant Purifiant là sản phẩm được thiết kế đặc biệt cho da dầu và da mụn. Với công thức chứa zinc PCA, sản phẩm giúp làm sạch sâu da, loại bỏ bụi bẩn, dầu thừa và bã nhờn, giúp thông thoáng lỗ chân lông và ngăn ngừa mụn. La Roche-Posay Effaclar Gel Moussant Purifiant còn giúp kiểm soát lượng dầu thừa trên da, làm dịu da và giảm viêm. Sản phẩm không chứa xà phòng, không paraben và không gây kích ứng. Hãy làm sạch sâu và kiểm soát mụn với La Roche-Posay!",
            "url": "https://example.com/sua-rua-mat-la-roche-posay-effaclar.html"
        }
    ]

    sku_list = []
    for i, item in enumerate(data):
        item['id'] = str(i + 1)
        item['chunk_content'] = dedent(
            f"""product_name: {item['title']}
                category: {item['category_name']}
                sku: {item['sku']}
                price: {item['price']}
                description: {item['description']}
                url: {item['url']}"""
        )
        sku_list.append(item['sku'])
    
    print(sku_list)
    return data

def create_index(index_name :str=None):
    if pinecone_client.has_index(index_name) == False:
        pinecone_client.create_index_for_model(
            name=index_name,
            cloud='aws',
            region='us-east-1',
            embed={
                'model': 'llama-text-embed-v2',
                'field_map': {
                    'text': 'chunk_content'
                }
            }
        )

    return pinecone_client.Index(index_name)
        
def main():
    print("Create index...")
    index = create_index(os.getenv('PINECONE_INDEX_NAME', 'sales-agent-miracle-life'))

    # Upsert company info
    print("Upsert company info...")
    index.upsert_records(
        namespace=os.getenv('PINECONE_NAMESPACE_COMPANY', 'company-info'),
        records=company_info_data()
    )

    # Upsert product
    print("Upsert product info...")
    index.upsert_records(
        namespace=os.getenv('PINECONE_NAMESPACE_PRODUCT', 'product-info'),
        records=products_data()
    )
    print("Finished")

if __name__ == '__main__':
    main()
    