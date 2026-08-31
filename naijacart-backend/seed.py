from app import app, db
from models import Category, Product


# =========================================================
# CATEGORY DATA
# =========================================================

categories = [
    {
        "name": "Smartphones",
        "description": "Shop the latest smartphones from Apple, Samsung, Google, Tecno, Infinix and more.",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85"
    },
    {
        "name": "Laptops",
        "description": "Powerful laptops for school, work, business, gaming and everyday productivity.",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85"
    },
    {
        "name": "Gaming",
        "description": "Gaming consoles, controllers, headsets, mice and other gaming accessories.",
        "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=900&q=85"
    },
    {
        "name": "Audio",
        "description": "Premium headphones, earbuds, speakers and other audio products.",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=85"
    },
    {
        "name": "Smartwatches",
        "description": "Smartwatches for fitness, health tracking, notifications and everyday use.",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=85"
    },
    {
        "name": "Accessories",
        "description": "Chargers, cables, power banks, keyboards, mice, phone cases and more.",
        "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=900&q=85"
    }
]


# =========================================================
# SMARTPHONES
# =========================================================

smartphones = [

    {
        "name": "iPhone 15 Pro Max",
        "brand": "Apple",
        "category": "Smartphones",
        "price": 1250000,
        "old_price": 1400000,
        "discount": 11,
        "rating": 4.9,
        "description": "Premium Apple smartphone with a powerful processor, advanced camera system, large display and long battery life.",
        "image": "https://images.unsplash.com/photo-1696446701796-da61225697cc?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "category": "Smartphones",
        "price": 1180000,
        "old_price": 1320000,
        "discount": 10,
        "rating": 4.8,
        "description": "Premium Samsung flagship smartphone featuring a high-resolution display, powerful performance and advanced camera system.",
        "image": "https://images.unsplash.com/photo-1610945264803-c22b62d2a7b3?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Google Pixel 9 Pro",
        "brand": "Google",
        "category": "Smartphones",
        "price": 950000,
        "old_price": 1030000,
        "discount": 8,
        "rating": 4.8,
        "description": "Google flagship smartphone with advanced photography, smooth performance and intelligent Android features.",
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Tecno Camon 30 Pro",
        "brand": "Tecno",
        "category": "Smartphones",
        "price": 420000,
        "old_price": 480000,
        "discount": 12,
        "rating": 4.6,
        "description": "Feature-packed Tecno smartphone with a powerful camera system, vibrant display and strong everyday performance.",
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Infinix Note 40 Pro",
        "brand": "Infinix",
        "category": "Smartphones",
        "price": 350000,
        "old_price": 410000,
        "discount": 15,
        "rating": 4.5,
        "description": "Modern Infinix smartphone with a smooth display, fast charging and powerful everyday performance.",
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Xiaomi 14 Ultra",
        "brand": "Xiaomi",
        "category": "Smartphones",
        "price": 790000,
        "old_price": 870000,
        "discount": 9,
        "rating": 4.7,
        "description": "High-end Xiaomi smartphone with flagship performance, advanced cameras and a premium display.",
        "image": "https://images.unsplash.com/photo-1567581935884-3349723552ca?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "iPhone 15",
        "brand": "Apple",
        "category": "Smartphones",
        "price": 850000,
        "old_price": 920000,
        "discount": 7,
        "rating": 4.7,
        "description": "Modern Apple smartphone with excellent performance, advanced cameras and a bright high-quality display.",
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Samsung Galaxy A55",
        "brand": "Samsung",
        "category": "Smartphones",
        "price": 390000,
        "old_price": 450000,
        "discount": 13,
        "rating": 4.6,
        "description": "Stylish Samsung smartphone offering reliable performance, a bright display and capable cameras.",
        "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Tecno Phantom V Fold",
        "brand": "Tecno",
        "category": "Smartphones",
        "price": 980000,
        "old_price": 1090000,
        "discount": 10,
        "rating": 4.6,
        "description": "Premium foldable Tecno smartphone designed for multitasking, entertainment and powerful mobile productivity.",
        "image": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Infinix GT 20 Pro",
        "brand": "Infinix",
        "category": "Smartphones",
        "price": 410000,
        "old_price": 465000,
        "discount": 12,
        "rating": 4.5,
        "description": "Performance-focused Infinix smartphone designed for gaming, entertainment and smooth everyday use.",
        "image": "https://images.unsplash.com/photo-1556656793-08538906a9f8?auto=format&fit=crop&w=700&q=85"
    }
]


# =========================================================
# LAPTOPS
# =========================================================

laptops = [

    {
        "name": "MacBook Air M2",
        "category": "Laptops",
        "brand": "Apple",
        "price": 1250000,
        "old_price": 1350000,
        "discount": 7,
        "rating": 4.9,
        "description": "Apple MacBook Air powered by the M2 chip, featuring 8GB RAM, 256GB SSD and a 13.6-inch display. Lightweight and ideal for school, work and everyday productivity.",
        "image": "https://images.unsplash.com/photo-1517336714739-489689fd1ca8?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Dell XPS 13 Plus",
        "category": "Laptops",
        "brand": "Dell",
        "price": 1180000,
        "old_price": 1280000,
        "discount": 8,
        "rating": 4.8,
        "description": "Premium Dell laptop with 16GB RAM, 512GB SSD and a 13.4-inch display. Designed for productivity, business and demanding everyday tasks.",
        "image": "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "HP Spectre x360 14",
        "category": "Laptops",
        "brand": "HP",
        "price": 1050000,
        "old_price": 1150000,
        "discount": 9,
        "rating": 4.7,
        "description": "Versatile HP 2-in-1 laptop with 16GB RAM, 512GB SSD and a 14-inch OLED display. Great for productivity, creativity and entertainment.",
        "image": "https://images.unsplash.com/photo-1602080858428-57174f9431cf?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Lenovo ThinkPad X1 Carbon",
        "category": "Laptops",
        "brand": "Lenovo",
        "price": 950000,
        "old_price": 1040000,
        "discount": 9,
        "rating": 4.7,
        "description": "Professional Lenovo ThinkPad with 16GB RAM, 512GB SSD and a 14-inch display. Built for business users, students and everyday productivity.",
        "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "ASUS ZenBook 14 OLED",
        "category": "Laptops",
        "brand": "ASUS",
        "price": 720000,
        "old_price": 790000,
        "discount": 9,
        "rating": 4.6,
        "description": "Slim ASUS laptop featuring 16GB RAM, 512GB SSD and a 14-inch OLED display. Offers a sharp viewing experience for work, study and entertainment.",
        "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Acer Swift 3",
        "category": "Laptops",
        "brand": "Acer",
        "price": 530000,
        "old_price": 590000,
        "discount": 10,
        "rating": 4.5,
        "description": "Lightweight Acer laptop with 8GB RAM, 512GB SSD and a 14-inch display. A practical choice for students, office work and everyday computing.",
        "image": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "HP Pavilion 15",
        "category": "Laptops",
        "brand": "HP",
        "price": 590000,
        "old_price": 650000,
        "discount": 9,
        "rating": 4.5,
        "description": "HP Pavilion laptop with 16GB RAM, 512GB SSD and a large 15.6-inch display. Suitable for productivity, study, browsing and entertainment.",
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "ASUS TUF Gaming F15",
        "category": "Laptops",
        "brand": "ASUS",
        "price": 630000,
        "old_price": 700000,
        "discount": 10,
        "rating": 4.6,
        "description": "ASUS gaming laptop with 16GB RAM, 512GB SSD and a 15.6-inch display. Designed for gaming, multitasking and demanding applications.",
        "image": "https://images.unsplash.com/photo-1593642702749-b7d2a804fbcf?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Microsoft Surface Laptop 5",
        "category": "Laptops",
        "brand": "Microsoft",
        "price": 1100000,
        "old_price": 1200000,
        "discount": 8,
        "rating": 4.7,
        "description": "Sleek Microsoft Surface laptop with 8GB RAM, 256GB SSD and a 13.5-inch display. Perfect for productivity, study and everyday use.",
        "image": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Lenovo IdeaPad Slim 3",
        "category": "Laptops",
        "brand": "Lenovo",
        "price": 620000,
        "old_price": 680000,
        "discount": 9,
        "rating": 4.5,
        "description": "Affordable Lenovo laptop with 8GB RAM, 512GB SSD and a 15.6-inch display. Great for students, home users and everyday productivity.",
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=700&q=85"
    }
]


# =========================================================
# GAMING
# =========================================================

gaming = [

    {
        "name": "PlayStation 5",
        "category": "Gaming",
        "brand": "PlayStation",
        "price": 950000,
        "old_price": 1050000,
        "discount": 10,
        "rating": 4.9,
        "description": "Powerful next-generation gaming console with 825GB SSD, 4K gaming and Ultra HD support.",
        "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Xbox Series X",
        "category": "Gaming",
        "brand": "Xbox",
        "price": 850000,
        "old_price": 930000,
        "discount": 9,
        "rating": 4.8,
        "description": "High-performance Xbox console with 1TB SSD, 4K gaming and up to 120 FPS.",
        "image": "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Nintendo Switch OLED",
        "category": "Gaming",
        "brand": "Nintendo",
        "price": 480000,
        "old_price": 530000,
        "discount": 9,
        "rating": 4.7,
        "description": "Portable gaming console featuring a vibrant OLED display, 64GB storage and flexible gaming modes.",
        "image": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "ASUS ROG Ally",
        "category": "Gaming",
        "brand": "ASUS",
        "price": 720000,
        "old_price": 790000,
        "discount": 9,
        "rating": 4.6,
        "description": "Powerful portable gaming device with 16GB RAM, 512GB SSD and a smooth 120Hz display.",
        "image": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Steam Deck OLED",
        "category": "Gaming",
        "brand": "Steam",
        "price": 690000,
        "old_price": 750000,
        "discount": 8,
        "rating": 4.7,
        "description": "Portable PC gaming console with 512GB SSD, OLED display and excellent handheld gaming performance.",
        "image": "https://images.unsplash.com/photo-1605901309584-818e25960a8f?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "PS5 DualSense Controller",
        "category": "Gaming",
        "brand": "PlayStation",
        "price": 125000,
        "old_price": 145000,
        "discount": 14,
        "rating": 4.8,
        "description": "Wireless PS5 controller with immersive haptic feedback, adaptive triggers and USB-C connectivity.",
        "image": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Xbox Wireless Controller",
        "category": "Gaming",
        "brand": "Xbox",
        "price": 105000,
        "old_price": 120000,
        "discount": 13,
        "rating": 4.7,
        "description": "Comfortable wireless gaming controller with Bluetooth support for Xbox Series X/S and compatible devices.",
        "image": "https://images.unsplash.com/photo-1628832307345-7404b47f6f7c?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Logitech G Pro X Headset",
        "category": "Gaming",
        "brand": "Logitech",
        "price": 165000,
        "old_price": 190000,
        "discount": 13,
        "rating": 4.7,
        "description": "Professional gaming headset with 7.1 surround sound, Blue VO!CE microphone technology and wired connectivity.",
        "image": "https://images.unsplash.com/photo-1599669454699-248893623440?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Razer BlackShark V2",
        "category": "Gaming",
        "brand": "Razer",
        "price": 135000,
        "old_price": 155000,
        "discount": 13,
        "rating": 4.6,
        "description": "Gaming headset with 7.1 surround sound, noise isolation and a comfortable wired design.",
        "image": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Logitech G502 Gaming Mouse",
        "category": "Gaming",
        "brand": "Logitech",
        "price": 95000,
        "old_price": 110000,
        "discount": 14,
        "rating": 4.6,
        "description": "High-performance gaming mouse with up to 25K DPI, RGB lighting and programmable buttons.",
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=700&q=85"
    }
]


# =========================================================
# AUDIO
# =========================================================

audio = [

    {
        "name": "Apple AirPods Pro 2",
        "category": "Audio",
        "brand": "Apple",
        "price": 420000,
        "old_price": 470000,
        "discount": 11,
        "rating": 4.8,
        "description": "Premium wireless earbuds with USB-C, active noise cancellation and Spatial Audio.",
        "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Sony WH-1000XM5",
        "category": "Audio",
        "brand": "Sony",
        "price": 580000,
        "old_price": 650000,
        "discount": 11,
        "rating": 4.9,
        "description": "Premium wireless headphones with advanced noise cancellation, 30-hour battery life and immersive sound.",
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Apple AirPods Max",
        "category": "Audio",
        "brand": "Apple",
        "price": 850000,
        "old_price": 930000,
        "discount": 9,
        "rating": 4.8,
        "description": "High-end over-ear headphones featuring Hi-Fi audio, Active Noise Cancellation and Spatial Audio.",
        "image": "https://images.unsplash.com/photo-1625245488600-2f7d2b9f1f83?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Samsung Galaxy Buds3 Pro",
        "category": "Audio",
        "brand": "Samsung",
        "price": 310000,
        "old_price": 350000,
        "discount": 11,
        "rating": 4.7,
        "description": "Premium Samsung earbuds with Hi-Fi sound, Active Noise Cancellation and wireless connectivity.",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "JBL Charge 5",
        "category": "Audio",
        "brand": "JBL",
        "price": 260000,
        "old_price": 295000,
        "discount": 12,
        "rating": 4.7,
        "description": "Portable Bluetooth speaker with powerful sound, waterproof construction and up to 20 hours of battery life.",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "JBL Tune 770NC",
        "category": "Audio",
        "brand": "JBL",
        "price": 190000,
        "old_price": 220000,
        "discount": 14,
        "rating": 4.6,
        "description": "Wireless headphones with adaptive noise cancellation, Bluetooth connectivity and up to 70 hours of battery life.",
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Bose QuietComfort Ultra",
        "category": "Audio",
        "brand": "Bose",
        "price": 690000,
        "old_price": 760000,
        "discount": 9,
        "rating": 4.8,
        "description": "Premium wireless headphones with immersive audio, advanced noise cancellation and Bluetooth connectivity.",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Sony WF-1000XM5",
        "category": "Audio",
        "brand": "Sony",
        "price": 465000,
        "old_price": 520000,
        "discount": 11,
        "rating": 4.8,
        "description": "Premium wireless earbuds with noise cancellation, Hi-Res Audio and a compact comfortable design.",
        "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Anker Soundcore Liberty 4",
        "category": "Audio",
        "brand": "Anker",
        "price": 185000,
        "old_price": 215000,
        "discount": 14,
        "rating": 4.5,
        "description": "Wireless earbuds with Hi-Res Audio, Active Noise Cancellation and dual-driver technology.",
        "image": "https://images.unsplash.com/photo-1598331668826-20cecc596b86?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Marshall Emberton II",
        "category": "Audio",
        "brand": "Marshall",
        "price": 330000,
        "old_price": 370000,
        "discount": 11,
        "rating": 4.7,
        "description": "Portable Bluetooth speaker with over 30 hours of battery life, powerful sound and a classic Marshall design.",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=700&q=85"
    }
]


# =========================================================
# SMARTWATCHES
# =========================================================

smartwatches = [

    {
        "name": "Apple Watch Series 9",
        "category": "Smartwatches",
        "brand": "Apple",
        "price": 650000,
        "old_price": 720000,
        "discount": 10,
        "rating": 4.8,
        "description": "Premium smartwatch with GPS, a 45mm Retina display, fitness tracking, notifications and advanced everyday features.",
        "image": "https://images.unsplash.com/photo-1551816230-ef5deaed4a26?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Samsung Galaxy Watch 6",
        "category": "Smartwatches",
        "brand": "Samsung",
        "price": 420000,
        "old_price": 470000,
        "discount": 11,
        "rating": 4.7,
        "description": "Stylish 44mm AMOLED smartwatch with health tracking, fitness features, notifications and powerful everyday performance.",
        "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Huawei Watch GT 4",
        "category": "Smartwatches",
        "brand": "Huawei",
        "price": 350000,
        "old_price": 390000,
        "discount": 10,
        "rating": 4.6,
        "description": "Elegant 46mm smartwatch featuring an AMOLED display, advanced fitness tracking and up to 14 days of battery life.",
        "image": "https://images.unsplash.com/photo-1579586337278-3f436f25d4d4?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Xiaomi Watch 2 Pro",
        "category": "Smartwatches",
        "brand": "Xiaomi",
        "price": 390000,
        "old_price": 430000,
        "discount": 9,
        "rating": 4.6,
        "description": "Powerful AMOLED smartwatch with GPS, Google Wear OS, fitness tracking and smart features for everyday use.",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Amazfit GTR 4",
        "category": "Smartwatches",
        "brand": "Amazfit",
        "price": 275000,
        "old_price": 310000,
        "discount": 11,
        "rating": 4.6,
        "description": "Fitness-focused smartwatch with an AMOLED display, GPS, health monitoring and comprehensive activity tracking.",
        "image": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Garmin Venu 3",
        "category": "Smartwatches",
        "brand": "Garmin",
        "price": 520000,
        "old_price": 570000,
        "discount": 9,
        "rating": 4.8,
        "description": "Advanced fitness smartwatch with an AMOLED display, GPS, health monitoring and detailed workout tracking.",
        "image": "https://images.unsplash.com/photo-1617625802912-cde586faf331?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Fitbit Versa 4",
        "category": "Smartwatches",
        "brand": "Fitbit",
        "price": 245000,
        "old_price": 280000,
        "discount": 13,
        "rating": 4.5,
        "description": "Fitness smartwatch with AMOLED display, activity tracking, sleep monitoring and useful health-focused features.",
        "image": "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Samsung Galaxy Watch 5 Pro",
        "category": "Smartwatches",
        "brand": "Samsung",
        "price": 450000,
        "old_price": 500000,
        "discount": 10,
        "rating": 4.7,
        "description": "Durable titanium smartwatch with GPS, long battery life, fitness tracking and premium health features.",
        "image": "https://images.unsplash.com/photo-1510017803434-a899398421b3?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Apple Watch SE",
        "category": "Smartwatches",
        "brand": "Apple",
        "price": 430000,
        "old_price": 480000,
        "discount": 10,
        "rating": 4.6,
        "description": "Affordable Apple smartwatch with GPS, a 44mm display, fitness tracking, notifications and essential smart features.",
        "image": "https://images.unsplash.com/photo-1617043786394-f977fa12eddf?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Xiaomi Redmi Watch 4",
        "category": "Smartwatches",
        "brand": "Xiaomi",
        "price": 185000,
        "old_price": 210000,
        "discount": 12,
        "rating": 4.5,
        "description": "Affordable smartwatch with a large 1.97-inch AMOLED display, GPS, fitness tracking and long battery life.",
        "image": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?auto=format&fit=crop&w=700&q=85"
    }
]


# =========================================================
# ACCESSORIES
# =========================================================

accessories = [

    {
        "name": "Anker 737 Power Bank",
        "category": "Accessories",
        "brand": "Anker",
        "price": 145000,
        "old_price": 165000,
        "discount": 12,
        "rating": 4.7,
        "description": "High-capacity 24,000mAh power bank with 140W fast charging, USB-C connectivity and advanced power management.",
        "image": "https://images.unsplash.com/photo-1609592424854-8f3e8a1f1d5b?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Apple USB-C Cable",
        "category": "Accessories",
        "brand": "Apple",
        "price": 45000,
        "old_price": 52000,
        "discount": 13,
        "rating": 4.6,
        "description": "Premium USB-C charging cable designed for fast charging, reliable data transfer and everyday Apple devices.",
        "image": "https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Samsung 45W Super Fast Charger",
        "category": "Accessories",
        "brand": "Samsung",
        "price": 55000,
        "old_price": 65000,
        "discount": 15,
        "rating": 4.7,
        "description": "45W USB-C Super Fast Charger designed to provide efficient and reliable fast charging for compatible Samsung devices.",
        "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "UGREEN 100W GaN Charger",
        "category": "Accessories",
        "brand": "UGREEN",
        "price": 85000,
        "old_price": 100000,
        "discount": 15,
        "rating": 4.7,
        "description": "Compact 100W GaN multi-port charger offering powerful USB-C fast charging for phones, tablets and laptops.",
        "image": "https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Baseus USB-C Fast Cable",
        "category": "Accessories",
        "brand": "Baseus",
        "price": 28000,
        "old_price": 35000,
        "discount": 20,
        "rating": 4.5,
        "description": "Durable braided USB-C to USB-C cable supporting up to 100W fast charging and reliable everyday connectivity.",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "iPhone MagSafe Case",
        "category": "Accessories",
        "brand": "Apple",
        "price": 38000,
        "old_price": 45000,
        "discount": 16,
        "rating": 4.5,
        "description": "Premium MagSafe-compatible iPhone case with shock protection, precise fitting and a sleek protective finish.",
        "image": "https://images.unsplash.com/photo-1603313011101-320f26a4f6f6?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Logitech MX Master 3S",
        "category": "Accessories",
        "brand": "Logitech",
        "price": 120000,
        "old_price": 140000,
        "discount": 14,
        "rating": 4.8,
        "description": "Advanced wireless mouse featuring high-precision tracking, Bluetooth connectivity and an ergonomic professional design.",
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Logitech MX Mechanical Keyboard",
        "category": "Accessories",
        "brand": "Logitech",
        "price": 155000,
        "old_price": 180000,
        "discount": 14,
        "rating": 4.7,
        "description": "Premium wireless mechanical keyboard with backlit keys, comfortable switches and a professional compact design.",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Anker PowerCore 20K",
        "category": "Accessories",
        "brand": "Anker",
        "price": 65000,
        "old_price": 75000,
        "discount": 13,
        "rating": 4.6,
        "description": "20,000mAh portable power bank with fast charging, USB-C connectivity and enough capacity for everyday mobile use.",
        "image": "https://images.unsplash.com/photo-1609592424854-8f3e8a1f1d5b?auto=format&fit=crop&w=700&q=85"
    },

    {
        "name": "Belkin BoostCharge Wireless Charger",
        "category": "Accessories",
        "brand": "Belkin",
        "price": 70000,
        "old_price": 80000,
        "discount": 13,
        "rating": 4.5,
        "description": "Convenient 15W wireless charger with Qi compatibility for fast and reliable charging of compatible smartphones.",
        "image": "https://images.unsplash.com/photo-1587033411391-5d9e51cce126?auto=format&fit=crop&w=700&q=85"
    }
]


# =========================================================
# COMBINE ALL PRODUCTS
# =========================================================

all_products = (
    smartphones
    + laptops
    + gaming
    + audio
    + smartwatches
    + accessories
)


# =========================================================
# SEED DATABASE
# =========================================================

def seed_database():

    with app.app_context():

        print("\n========================================")
        print("      NAIJACART DATABASE SEED")
        print("========================================\n")

        # -------------------------------------------------
        # CREATE / UPDATE CATEGORIES
        # -------------------------------------------------

        category_map = {}

        for category_data in categories:

            category = Category.query.filter_by(
                name=category_data["name"]
            ).first()

            if not category:

                category = Category(
                    name=category_data["name"],
                    description=category_data["description"],
                    image_url=category_data["image_url"]
                )

                db.session.add(category)
                db.session.flush()

                print(
                    f"Category created: {category.name}"
                )

            else:

                category.description = category_data["description"]
                category.image_url = category_data["image_url"]

            category_map[category.name] = category


        # -------------------------------------------------
        # CREATE / UPDATE PRODUCTS
        # -------------------------------------------------

        created = 0
        updated = 0

        for data in all_products:

            product = Product.query.filter_by(
                name=data["name"]
            ).first()

            category = category_map[
                data["category"]
            ]

            if product:

                # Update existing product
                product.brand = data["brand"]
                product.description = data["description"]
                product.price = data["price"]
                product.old_price = data["old_price"]
                product.discount = data["discount"]
                product.rating = data["rating"]
                product.category = data["category"]
                product.category_id = category.id
                product.image_url = data["image"]

                # Only set stock if it is empty/zero
                if not product.stock:
                    product.stock = 10

                updated += 1

            else:

                product = Product(
                    name=data["name"],
                    brand=data["brand"],
                    description=data["description"],
                    price=data["price"],
                    old_price=data["old_price"],
                    discount=data["discount"],
                    rating=data["rating"],
                    category=data["category"],
                    category_id=category.id,
                    image_url=data["image"],
                    stock=10
                )

                db.session.add(product)

                created += 1


        # -------------------------------------------------
        # SAVE CHANGES
        # -------------------------------------------------

        db.session.commit()


        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        print("\n========================================")
        print("       SEED COMPLETED SUCCESSFULLY")
        print("========================================")
        print(f"Categories: {Category.query.count()}")
        print(f"Products:   {Product.query.count()}")
        print(f"Created:    {created}")
        print(f"Updated:    {updated}")
        print("========================================\n")


# =========================================================
# RUN SEED
# =========================================================

if __name__ == "__main__":
    seed_database()