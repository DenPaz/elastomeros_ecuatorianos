# ruff: noqa: E501
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from slugify import slugify

from apps.products.models import Attribute
from apps.products.models import AttributeValue
from apps.products.models import Category
from apps.products.models import Product
from apps.products.models import ProductVariant
from apps.products.models import ProductVariantAttributeValue

data = [
    {
        "category_name": "Latex",
        "name": "Latex cremado",
        "slug": "latex-cremado",
        "short_description": (
            "Latex natural en estado cremoso, ideal para la "
            "fabricación de guantes y otros productos de caucho."
        ),
        "full_description": (
            "El latex cremado es un material versátil y de alta "
            "calidad, obtenido del látex natural del árbol de "
            "caucho. Su consistencia cremosa facilita su "
            "manipulación y procesamiento en la fabricación de "
            "diversos productos de caucho, como guantes, "
            "condones y artículos médicos. Este tipo de látex "
            "ofrece excelentes propiedades elásticas y de "
            "resistencia, asegurando la durabilidad y "
            "confort en los productos finales."
        ),
        "is_active": True,
        "variants": [
            {
                "sku": "LTX-CREM-1GAL",
                "price": "25.00",
                "stock": 35,
                "attributes": {
                    "Volumen del recipiente": "1 Galón",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "LTX-CREM-5GAL",
                "price": "110.00",
                "stock": 20,
                "attributes": {
                    "Volumen del recipiente": "5 Galones",
                },
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Guantes de caucho natural domésticos",
        "slug": "guantes-de-caucho-natural-domesticos",
        "short_description": (
            "Guantes de caucho natural diseñados para uso "
            "doméstico, ideales para tareas de limpieza y "
            "protección de las manos."
        ),
        "full_description": (
            "Nuestros guantes de caucho natural domésticos son "
            "la elección perfecta para proteger tus manos durante "
            "las tareas del hogar. Fabricados con caucho natural "
            "de alta calidad, estos guantes ofrecen una excelente "
            "elasticidad y resistencia, asegurando comodidad y "
            "durabilidad. Son ideales para lavar platos, limpiar "
            "superficies y manejar productos químicos domésticos, "
            "proporcionando una barrera efectiva contra la suciedad "
            "y los agentes irritantes. Disponibles en varios tamaños "
            "y colores, nuestros guantes se adaptan a tus necesidades "
            "diarias de limpieza."
        ),
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-DOM-AMAR-7",
                "price": "1.00",
                "stock": 100,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-75",
                "price": "1.00",
                "stock": 70,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7.5",
                },
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-8",
                "price": "1.00",
                "stock": 80,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8",
                },
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-85",
                "price": "1.00",
                "stock": 60,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8.5",
                },
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "GUANT-DOM-AMAR-9",
                "price": "1.00",
                "stock": 90,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "9",
                },
                "sort_order": 4,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Guantes de caucho natural semi-industriales",
        "slug": "guantes-de-caucho-natural-semi-industriales",
        "short_description": (
            "Guantes de caucho natural diseñados para uso "
            "semi-industrial, ideales para tareas que requieren "
            "mayor resistencia y protección."
        ),
        "full_description": (
            "Nuestros guantes de caucho natural semi-industriales "
            "están diseñados para ofrecer una protección superior "
            "en entornos de trabajo que demandan mayor resistencia. "
            "Fabricados con caucho natural de alta calidad, estos "
            "guantes proporcionan una excelente elasticidad y durabilidad, "
            "asegurando comodidad durante largas jornadas laborales. "
            "Son ideales para tareas de manipulación de materiales, "
            "trabajos de construcción y otras actividades semi-industriales "
            "donde se requiere una barrera efectiva contra abrasiones, "
            "cortes y productos químicos. Disponibles en varios tamaños "
            "y colores, nuestros guantes se adaptan a las necesidades "
            "específicas de tu entorno de trabajo."
        ),
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-SEMI-AMAR-7",
                "price": "1.30",
                "stock": 50,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-75",
                "price": "1.30",
                "stock": 40,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "7.5",
                },
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-8",
                "price": "1.30",
                "stock": 60,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8",
                },
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-85",
                "price": "1.30",
                "stock": 30,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "8.5",
                },
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "GUANT-SEMI-AMAR-9",
                "price": "1.30",
                "stock": 70,
                "attributes": {
                    "Color de guantes": "Amarillo",
                    "Tamaño de guantes": "9",
                },
                "sort_order": 4,
                "is_active": True,
            },
        ],
    },
]
dummy_data = [
    {
        "category_name": "Adhesivos y Selladores",
        "name": "Sellador de Poliuretano 300ml",
        "slug": "sellador-poliuretano-300ml",
        "short_description": "Sellador elástico de alta adherencia para juntas.",
        "full_description": "Ideal para sellar juntas de construcción, grietas y fisuras. Ofrece una excelente resistencia a la intemperie y al envejecimiento. Curado rápido y pintable.",
        "is_active": True,
        "variants": [
            {
                "sku": "SEL-POL-300-BLC",
                "price": "8.50",
                "stock": 150,
                "attributes": {"Color": "Blanco"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "SEL-POL-300-GRS",
                "price": "8.50",
                "stock": 120,
                "attributes": {"Color": "Gris"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "SEL-POL-300-NGR",
                "price": "8.50",
                "stock": 90,
                "attributes": {"Color": "Negro"},
                "sort_order": 2,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Calzado de Seguridad",
        "name": "Bota de Seguridad Punta de Acero",
        "slug": "bota-seguridad-punta-acero",
        "short_description": "Bota de trabajo robusta con protección dieléctrica.",
        "full_description": "Fabricada en cuero de alta resistencia, con suela antideslizante y punta de acero para máxima protección en entornos industriales. Cumple con normas de seguridad.",
        "is_active": True,
        "variants": [
            {
                "sku": "CALZ-SEG-PNT-39",
                "price": "45.00",
                "stock": 30,
                "attributes": {"Talla de Calzado": "39", "Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "CALZ-SEG-PNT-40",
                "price": "45.00",
                "stock": 40,
                "attributes": {"Talla de Calzado": "40", "Color": "Negro"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "CALZ-SEG-PNT-41",
                "price": "45.00",
                "stock": 50,
                "attributes": {"Talla de Calzado": "41", "Color": "Negro"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "CALZ-SEG-PNT-42",
                "price": "45.00",
                "stock": 50,
                "attributes": {"Talla de Calzado": "42", "Color": "Negro"},
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "CALZ-SEG-PNT-43",
                "price": "45.00",
                "stock": 30,
                "attributes": {"Talla de Calzado": "43", "Color": "Negro"},
                "sort_order": 4,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Mangueras Industriales",
        "name": "Manguera de Riego Reforzada",
        "slug": "manguera-riego-reforzada",
        "short_description": "Manguera de PVC flexible con refuerzo de poliéster.",
        "full_description": "Diseñada para uso agrícola e industrial. Alta resistencia a la abrasión y a la presión. Flexible y fácil de manejar en todas las condiciones climáticas.",
        "is_active": True,
        "variants": [
            {
                "sku": "MANG-RIE-1/2-25M",
                "price": "18.00",
                "stock": 50,
                "attributes": {"Diámetro Interno": "1/2 pulgada", "Longitud": "25m"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "MANG-RIE-1/2-50M",
                "price": "35.00",
                "stock": 30,
                "attributes": {"Diámetro Interno": "1/2 pulgada", "Longitud": "50m"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "MANG-RIE-3/4-25M",
                "price": "25.00",
                "stock": 40,
                "attributes": {"Diámetro Interno": "3/4 pulgada", "Longitud": "25m"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "MANG-RIE-3/4-50M",
                "price": "48.00",
                "stock": 20,
                "attributes": {"Diámetro Interno": "3/4 pulgada", "Longitud": "50m"},
                "sort_order": 3,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Pisos y Revestimientos",
        "name": "Piso de Caucho Antideslizante (Metro Cuadrado)",
        "slug": "piso-caucho-antideslizante-m2",
        "short_description": "Piso de caucho tipo moneda para alto tráfico.",
        "full_description": "Revestimiento de caucho vulcanizado de alta durabilidad, ideal para gimnasios, talleres, y zonas de juego. Fácil de instalar y limpiar. Se vende por metro cuadrado.",
        "is_active": True,
        "variants": [
            {
                "sku": "PISO-CAU-MON-NGR",
                "price": "12.50",
                "stock": 500,
                "attributes": {"Color": "Negro", "Espesor": "3mm"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "PISO-CAU-MON-GRS",
                "price": "13.00",
                "stock": 300,
                "attributes": {"Color": "Gris", "Espesor": "3mm"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "PISO-CAU-MON-AZL",
                "price": "13.00",
                "stock": 200,
                "attributes": {"Color": "Azul", "Espesor": "3mm"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "PISO-CAU-MON-NGR-5MM",
                "price": "16.50",
                "stock": 150,
                "attributes": {"Color": "Negro", "Espesor": "5mm"},
                "sort_order": 3,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Casco de Seguridad Dieléctrico",
        "slug": "casco-seguridad-dielectrico",
        "short_description": "Casco de protección industrial con suspensión de 4 puntos.",
        "full_description": "Casco ligero y resistente, diseñado para proteger contra impactos y descargas eléctricas. Cumple con la norma ANSI Z89.1 Tipo I, Clase E.",
        "is_active": True,
        "variants": [
            {
                "sku": "EPP-CASCO-BLC",
                "price": "11.00",
                "stock": 80,
                "attributes": {"Color": "Blanco"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "EPP-CASCO-AMR",
                "price": "11.00",
                "stock": 60,
                "attributes": {"Color": "Amarillo"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "EPP-CASCO-AZL",
                "price": "11.00",
                "stock": 50,
                "attributes": {"Color": "Azul"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "EPP-CASCO-RJO",
                "price": "11.00",
                "stock": 30,
                "attributes": {"Color": "Rojo"},
                "sort_order": 3,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Adhesivos y Selladores",
        "name": "Adhesivo de Contacto 1 Galón",
        "slug": "adhesivo-contacto-1-galon",
        "short_description": "Adhesivo de alto rendimiento para madera, caucho y cuero.",
        "full_description": "Adhesivo de secado rápido y fuerte agarre. Ideal para trabajos de carpintería, tapicería y reparaciones generales. Resistente al calor y la humedad.",
        "is_active": True,
        "variants": [
            {
                "sku": "ADH-CONT-1GAL",
                "price": "22.00",
                "stock": 45,
                "attributes": {
                    "Volumen del recipiente": "1 Galón",
                    "Tipo de Adhesivo": "de Contacto",
                },
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Guantes de Nitrilo Desechables (Caja 100u)",
        "slug": "guantes-nitrilo-desechables-100u",
        "short_description": "Guantes finos para uso médico o alimenticio, sin polvo.",
        "full_description": "Caja de 100 guantes de nitrilo ambidiestros, libres de látex y polvo. Ofrecen excelente sensibilidad táctil y protección contra bacterias y químicos.",
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-NIT-DES-S",
                "price": "9.50",
                "stock": 200,
                "attributes": {"Tamaño de guantes": "S", "Color": "Azul"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-NIT-DES-M",
                "price": "9.50",
                "stock": 300,
                "attributes": {"Tamaño de guantes": "M", "Color": "Azul"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-NIT-DES-L",
                "price": "9.50",
                "stock": 250,
                "attributes": {"Tamaño de guantes": "L", "Color": "Azul"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "GUANT-NIT-DES-XL",
                "price": "9.50",
                "stock": 100,
                "attributes": {"Tamaño de guantes": "XL", "Color": "Azul"},
                "sort_order": 3,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Gafas de Seguridad Anti-empañantes",
        "slug": "gafas-seguridad-antiempanantes",
        "short_description": "Gafas de policarbonato con protección UV y anti-rayaduras.",
        "full_description": "Protección ocular ligera y cómoda. Lentes claros con tratamiento anti-empañante y filtro UV 99.9%. Patillas ajustables para un ajuste perfecto.",
        "is_active": True,
        "variants": [
            {
                "sku": "EPP-GAF-CLARO",
                "price": "3.50",
                "stock": 300,
                "attributes": {"Color": "Transparente"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "EPP-GAF-OSCURO",
                "price": "3.75",
                "stock": 150,
                "attributes": {"Color": "Gris"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Mangueras Industriales",
        "name": "Manguera para Aire Comprimido 10 Bar",
        "slug": "manguera-aire-comprimido-10bar",
        "short_description": "Manguera de caucho sintético para herramientas neumáticas.",
        "full_description": "Manguera robusta para líneas de aire comprimido en talleres e industria. Resistente a aceites y abrasión. Incluye acoples rápidos.",
        "is_active": True,
        "variants": [
            {
                "sku": "MANG-AIRE-1/4-10M",
                "price": "28.00",
                "stock": 40,
                "attributes": {"Diámetro Interno": "1/4 pulgada", "Longitud": "10m"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "MANG-AIRE-1/4-20M",
                "price": "55.00",
                "stock": 20,
                "attributes": {"Diámetro Interno": "1/4 pulgada", "Longitud": "20m"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "MANG-AIRE-3/8-10M",
                "price": "35.00",
                "stock": 35,
                "attributes": {"Diámetro Interno": "3/8 pulgada", "Longitud": "10m"},
                "sort_order": 2,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Pisos y Revestimientos",
        "name": "Piso Dieléctrico Aislante (Rollo 10m)",
        "slug": "piso-dielectrico-aislante-10m",
        "short_description": "Piso de caucho aislante para tableros eléctricos.",
        "full_description": "Rollo de 1m de ancho por 10m de largo. Diseñado para proteger al personal de descargas eléctricas en áreas de alto voltaje. Clase 2 (17,000V).",
        "is_active": True,
        "variants": [
            {
                "sku": "PISO-DIEL-CL2-NGR",
                "price": "450.00",
                "stock": 10,
                "attributes": {"Color": "Negro", "Espesor": "4mm"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "PISO-DIEL-CL2-GRS",
                "price": "450.00",
                "stock": 5,
                "attributes": {"Color": "Gris", "Espesor": "4mm"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Calzado de Seguridad",
        "name": "Bota de PVC Blanca Sanitaria",
        "slug": "bota-pvc-blanca-sanitaria",
        "short_description": "Bota impermeable para industria alimentaria o laboratorios.",
        "full_description": "Bota de caña alta fabricada en PVC, 100% impermeable. Fácil de limpiar y desinfectar. Suela antideslizante resistente a grasas y aceites.",
        "is_active": True,
        "variants": [
            {
                "sku": "CALZ-PVC-BL-38",
                "price": "19.90",
                "stock": 25,
                "attributes": {"Talla de Calzado": "38", "Color": "Blanco"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-BL-39",
                "price": "19.90",
                "stock": 30,
                "attributes": {"Talla de Calzado": "39", "Color": "Blanco"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-BL-40",
                "price": "19.90",
                "stock": 40,
                "attributes": {"Talla de Calzado": "40", "Color": "Blanco"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-BL-41",
                "price": "19.90",
                "stock": 40,
                "attributes": {"Talla de Calzado": "41", "Color": "Blanco"},
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-BL-42",
                "price": "19.90",
                "stock": 35,
                "attributes": {"Talla de Calzado": "42", "Color": "Blanco"},
                "sort_order": 4,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Adhesivos y Selladores",
        "name": "Silicona Acética Transparente 280ml",
        "slug": "silicona-acetica-transparente-280ml",
        "short_description": "Sellador de silicona para baños y cocinas.",
        "full_description": "Forma un sello flexible e impermeable, resistente a la formación de hongos. Ideal para sellar alrededor de lavabos, bañeras y ventanas.",
        "is_active": True,
        "variants": [
            {
                "sku": "SIL-ACE-280-TR",
                "price": "4.20",
                "stock": 250,
                "attributes": {"Color": "Transparente", "Tipo de Adhesivo": "Silicona"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "SIL-ACE-280-BL",
                "price": "4.20",
                "stock": 180,
                "attributes": {"Color": "Blanco", "Tipo de Adhesivo": "Silicona"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Guante de Nitrilo Industrial (Par)",
        "slug": "guante-nitrilo-industrial-par",
        "short_description": "Guante robusto resistente a químicos y solventes.",
        "full_description": "Guante de nitrilo de 13 pulgadas de largo, calibre 15. Ofrece protección superior contra aceites, grasas, ácidos y solventes. Interior flocado para mayor comodidad.",
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-IND-NIT-8",
                "price": "2.10",
                "stock": 120,
                "attributes": {"Tamaño de guantes": "8", "Color": "Verde"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-IND-NIT-9",
                "price": "2.10",
                "stock": 150,
                "attributes": {"Tamaño de guantes": "9", "Color": "Verde"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-IND-NIT-10",
                "price": "2.10",
                "stock": 100,
                "attributes": {"Tamaño de guantes": "10", "Color": "Verde"},
                "sort_order": 2,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Mangueras Industriales",
        "name": "Manguera Succión y Descarga 2 pulgadas (por metro)",
        "slug": "manguera-succion-descarga-2-pulg-metro",
        "short_description": "Manguera de PVC corrugada para agua y lodos.",
        "full_description": "Manguera flexible y duradera para succión y descarga de agua, lodos ligeros y materiales abrasivos. Espiral de PVC rígido. Se vende por metro lineal.",
        "is_active": True,
        "variants": [
            {
                "sku": "MANG-SUC-2-M",
                "price": "7.80",
                "stock": 100,
                "attributes": {"Diámetro Interno": "2 pulgadas"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "MANG-SUC-3-M",
                "price": "11.20",
                "stock": 50,
                "attributes": {"Diámetro Interno": "3 pulgadas"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Plancha de Caucho SBR (m2)",
        "slug": "plancha-caucho-sbr-m2",
        "short_description": "Lámina de caucho SBR para uso general industrial.",
        "full_description": "Plancha de caucho SBR (estireno-butadieno) de 1m de ancho. Buena resistencia a la abrasión y al impacto. Ideal para juntas, sellos y pisos. Se vende por m2.",
        "is_active": True,
        "variants": [
            {
                "sku": "PLN-SBR-2MM-M2",
                "price": "9.00",
                "stock": 80,
                "attributes": {"Espesor": "2mm", "Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "PLN-SBR-3MM-M2",
                "price": "13.50",
                "stock": 60,
                "attributes": {"Espesor": "3mm", "Color": "Negro"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "PLN-SBR-5MM-M2",
                "price": "22.00",
                "stock": 40,
                "attributes": {"Espesor": "5mm", "Color": "Negro"},
                "sort_order": 2,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Arnés de Seguridad de Cuerpo Completo",
        "slug": "arnes-seguridad-cuerpo-completo",
        "short_description": "Arnés con 4 puntos de anclaje para trabajos en altura.",
        "full_description": "Arnés de seguridad ergonómico con anillas D en espalda y pecho. Cintas de poliéster ajustables en piernas y torso. Certificado para trabajos en altura.",
        "is_active": True,
        "variants": [
            {
                "sku": "EPP-ARNES-FULL-L",
                "price": "38.00",
                "stock": 25,
                "attributes": {"Talla de Arnés": "L/XL", "Color": "Rojo/Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "EPP-ARNES-FULL-M",
                "price": "38.00",
                "stock": 20,
                "attributes": {"Talla de Arnés": "S/M", "Color": "Rojo/Negro"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Adhesivos y Selladores",
        "name": "Adhesivo Epóxico Bicomponente 10 min",
        "slug": "adhesivo-epoxico-10-min",
        "short_description": "Pegamento extra fuerte de dos componentes.",
        "full_description": "Jeringa de 25ml. Mezcla y pega en 10 minutos. Une metales, cerámica, madera, vidrio y plásticos duros. Alta resistencia a la tracción.",
        "is_active": True,
        "variants": [
            {
                "sku": "ADH-EPOX-10MIN",
                "price": "5.50",
                "stock": 90,
                "attributes": {"Tipo de Adhesivo": "Epóxico", "Color": "Transparente"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Topes de Andén de Caucho",
        "slug": "topes-anden-caucho",
        "short_description": "Tope de caucho para protección de muelles de carga.",
        "full_description": "Bloque de caucho vulcanizado de alta densidad. Dimensiones 50cm x 15cm x 10cm. Absorbe impactos de camiones y protege la infraestructura del andén.",
        "is_active": True,
        "variants": [
            {
                "sku": "TOPE-ANDEN-50X15",
                "price": "18.00",
                "stock": 60,
                "attributes": {"Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Mangueras Industriales",
        "name": "Manguera de Grado Alimenticio (por metro)",
        "slug": "manguera-grado-alimenticio-metro",
        "short_description": "Manguera atóxica para transporte de líquidos.",
        "full_description": "Manguera de PVC transparente con refuerzo, aprobada por FDA para contacto con alimentos y bebidas. No altera el sabor ni el olor.",
        "is_active": True,
        "variants": [
            {
                "sku": "MANG-ALIM-3/4-M",
                "price": "4.50",
                "stock": 70,
                "attributes": {
                    "Diámetro Interno": "3/4 pulgada",
                    "Color": "Transparente",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "MANG-ALIM-1-M",
                "price": "5.80",
                "stock": 60,
                "attributes": {
                    "Diámetro Interno": "1 pulgada",
                    "Color": "Transparente",
                },
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Chaleco Reflectivo de Seguridad",
        "slug": "chaleco-reflectivo-seguridad",
        "short_description": "Chaleco de alta visibilidad con cintas reflectivas.",
        "full_description": "Chaleco tipo periodista fabricado en tela fluorescente con cintas reflectivas de 2 pulgadas. Cierre frontal. Ideal para trabajos viales y construcción.",
        "is_active": True,
        "variants": [
            {
                "sku": "EPP-CHALECO-NAR",
                "price": "4.80",
                "stock": 150,
                "attributes": {"Color": "Naranja"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "EPP-CHALECO-VER",
                "price": "4.80",
                "stock": 120,
                "attributes": {"Color": "Verde Fluorescente"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Pisos y Revestimientos",
        "name": "Cinta Antideslizante Adhesiva (Rollo 5m)",
        "slug": "cinta-antideslizante-adhesiva-5m",
        "short_description": "Cinta adhesiva con superficie abrasiva para gradas.",
        "full_description": "Rollo de 5 metros de largo y 2 pulgadas de ancho. Evita resbalones en gradas, rampas y superficies lisas. Adhesivo de alta duración.",
        "is_active": True,
        "variants": [
            {
                "sku": "CINTA-ANTI-5M-NGR",
                "price": "6.20",
                "stock": 90,
                "attributes": {"Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "CINTA-ANTI-5M-AMR",
                "price": "6.50",
                "stock": 60,
                "attributes": {"Color": "Amarillo/Negro"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Calzado de Seguridad",
        "name": "Zapato de Seguridad Dieléctrico Tipo Ejecutivo",
        "slug": "zapato-seguridad-dielectrico-ejecutivo",
        "short_description": "Zapato de seguridad ligero con punta de composite.",
        "full_description": "Diseño casual tipo ejecutivo, pero con toda la protección. Punta de composite (no metálica) y suela dieléctrica. Ultra ligero y cómodo.",
        "is_active": True,
        "variants": [
            {
                "sku": "CALZ-EJEC-COMP-40",
                "price": "55.00",
                "stock": 20,
                "attributes": {"Talla de Calzado": "40", "Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "CALZ-EJEC-COMP-41",
                "price": "55.00",
                "stock": 30,
                "attributes": {"Talla de Calzado": "41", "Color": "Negro"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "CALZ-EJEC-COMP-42",
                "price": "55.00",
                "stock": 25,
                "attributes": {"Talla de Calzado": "42", "Color": "Negro"},
                "sort_order": 2,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Guantes de Neopreno para Químicos (Par)",
        "slug": "guantes-neopreno-quimicos-par",
        "short_description": "Guantes de alta resistencia a ácidos y cáusticos.",
        "full_description": "Guantes de 18 pulgadas de largo, fabricados en neopreno sobre látex. Excelente protección contra un amplio espectro de productos químicos.",
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-NEO-CHEM-9",
                "price": "7.50",
                "stock": 50,
                "attributes": {"Tamaño de guantes": "9", "Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-NEO-CHEM-10",
                "price": "7.50",
                "stock": 40,
                "attributes": {"Tamaño de guantes": "10", "Color": "Negro"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Mascarilla de Media Cara con Filtros",
        "slug": "mascarilla-media-cara-filtros",
        "short_description": "Respirador reutilizable para vapores y partículas.",
        "full_description": "Mascarilla de elastómero termoplástico, cómoda y ligera. Incluye un par de cartuchos para vapores orgánicos (OV) y prefiltros P100.",
        "is_active": True,
        "variants": [
            {
                "sku": "EPP-MASK-MEDIA-M",
                "price": "29.99",
                "stock": 30,
                "attributes": {"Talla de Mascarilla": "M"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "EPP-MASK-MEDIA-L",
                "price": "29.99",
                "stock": 20,
                "attributes": {"Talla de Mascarilla": "L"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Mangueras Industriales",
        "name": 'Manguera de Descarga Plana (Lay Flat) 2"',
        "slug": "manguera-descarga-plana-2-pulg",
        "short_description": "Manguera azul de PVC para descarga de agua, rollo 50m.",
        "full_description": "Manguera flexible y liviana que se aplana al vaciarse para un fácil almacenamiento. Ideal para bombas sumergibles y aplicaciones de riego.",
        "is_active": True,
        "variants": [
            {
                "sku": "MANG-LAYFLAT-2-50M",
                "price": "65.00",
                "stock": 15,
                "attributes": {"Diámetro Interno": "2 pulgadas", "Longitud": "50m"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "MANG-LAYFLAT-3-50M",
                "price": "85.00",
                "stock": 10,
                "attributes": {"Diámetro Interno": "3 pulgadas", "Longitud": "50m"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Adhesivos y Selladores",
        "name": "Cinta de Embalaje Transparente (Paquete 6u)",
        "slug": "cinta-embalaje-transparente-6u",
        "short_description": "Cinta adhesiva de 48mm x 50m para sellado de cajas.",
        "full_description": "Paquete de 6 rollos de cinta de embalaje transparente. Adhesivo acrílico de alta adherencia para un sellado seguro y duradero de cajas de cartón.",
        "is_active": True,
        "variants": [
            {
                "sku": "CINTA-EMB-TR-6PK",
                "price": "5.99",
                "stock": 200,
                "attributes": {"Color": "Transparente"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Plancha de Neopreno (m2)",
        "slug": "plancha-neopreno-m2",
        "short_description": "Lámina de neopreno resistente a aceites y clima.",
        "full_description": "Plancha de neopreno de 1m de ancho. Excelente resistencia a aceites, grasas y condiciones climáticas. Ideal para juntas y sellos automotrices o marinos. Venta por m2.",
        "is_active": True,
        "variants": [
            {
                "sku": "PLN-NEO-2MM-M2",
                "price": "18.00",
                "stock": 30,
                "attributes": {"Espesor": "2mm", "Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "PLN-NEO-3MM-M2",
                "price": "26.00",
                "stock": 25,
                "attributes": {"Espesor": "3mm", "Color": "Negro"},
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Calzado de Seguridad",
        "name": "Bota de PVC Caña Alta (Industrial)",
        "slug": "bota-pvc-cana-alta-industrial",
        "short_description": "Bota negra con punta de acero, resistente a hidrocarburos.",
        "full_description": "Bota industrial fabricada en PVC/Nitrilo para resistir hidrocarburos, grasas y aceites. Incluye punta de acero y suela antideslizante.",
        "is_active": True,
        "variants": [
            {
                "sku": "CALZ-PVC-IND-39",
                "price": "24.50",
                "stock": 30,
                "attributes": {"Talla de Calzado": "39", "Color": "Negro"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-IND-40",
                "price": "24.50",
                "stock": 40,
                "attributes": {"Talla de Calzado": "40", "Color": "Negro"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-IND-41",
                "price": "24.50",
                "stock": 45,
                "attributes": {"Talla de Calzado": "41", "Color": "Negro"},
                "sort_order": 2,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-IND-42",
                "price": "24.50",
                "stock": 40,
                "attributes": {"Talla de Calzado": "42", "Color": "Negro"},
                "sort_order": 3,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-IND-43",
                "price": "24.50",
                "stock": 30,
                "attributes": {"Talla de Calzado": "43", "Color": "Negro"},
                "sort_order": 4,
                "is_active": True,
            },
            {
                "sku": "CALZ-PVC-IND-44",
                "price": "24.50",
                "stock": 20,
                "attributes": {"Talla de Calzado": "44", "Color": "Negro"},
                "sort_order": 5,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Protector Auditivo Tipo Copa",
        "slug": "protector-auditivo-tipo-copa",
        "short_description": "Orejeras de seguridad con NRR 25dB.",
        "full_description": "Protector auditivo tipo diadema, ligero y ajustable. Copas acolchadas para mayor comodidad durante el uso prolongado. Nivel de reducción de ruido (NRR) de 25 decibeles.",
        "is_active": True,
        "variants": [
            {
                "sku": "EPP-OREJERA-25DB",
                "price": "14.00",
                "stock": 70,
                "attributes": {"Color": "Rojo/Negro"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Adhesivos y Selladores",
        "name": "Cinta Adhesiva Doble Faz (Rollo 10m)",
        "slug": "cinta-doble-faz-10m",
        "short_description": "Cinta de espuma acrílica de alta adherencia.",
        "full_description": "Rollo de 10m x 19mm. Cinta de espuma de polietileno con adhesivo acrílico en ambas caras. Ideal para montajes ligeros, cartelería y manualidades.",
        "is_active": True,
        "variants": [
            {
                "sku": "CINTA-DBLFAZ-10M",
                "price": "3.80",
                "stock": 110,
                "attributes": {"Color": "Blanco"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Productos de caucho",
        "name": "Rompevelocidades de Caucho (Módulo)",
        "slug": "rompevelocidades-caucho-modulo",
        "short_description": "Módulo de 50cm para reductor de velocidad.",
        "full_description": "Módulo individual de reductor de velocidad. Fabricado en caucho reciclado de alta resistencia. Incluye cintas reflectivas amarillas. No incluye pernos de anclaje.",
        "is_active": True,
        "variants": [
            {
                "sku": "ROMPEVEL-MOD-50CM",
                "price": "16.00",
                "stock": 80,
                "attributes": {"Color": "Amarillo/Negro"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Equipamiento de Protección",
        "name": "Guante Anticorte Nivel 5 (Par)",
        "slug": "guante-anticorte-nivel-5-par",
        "short_description": "Guante de fibra HPPE con recubrimiento de PU.",
        "full_description": "Máxima protección contra cortes (Nivel 5 ANSI/ISEA). Recubrimiento de poliuretano en la palma para un excelente agarre en seco y húmedo.",
        "is_active": True,
        "variants": [
            {
                "sku": "GUANT-AC-N5-M",
                "price": "8.50",
                "stock": 60,
                "attributes": {"Tamaño de guantes": "M", "Color": "Gris"},
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "GUANT-AC-N5-L",
                "price": "8.50",
                "stock": 70,
                "attributes": {"Tamaño de guantes": "L", "Color": "Gris"},
                "sort_order": 1,
                "is_active": True,
            },
            {
                "sku": "GUANT-AC-N5-XL",
                "price": "8.50",
                "stock": 50,
                "attributes": {"Tamaño de guantes": "XL", "Color": "Gris"},
                "sort_order": 2,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Mangueras Industriales",
        "name": 'Manguera de PVC Transparente 1/4" (por metro)',
        "slug": "manguera-pvc-transparente-1-4-metro",
        "short_description": "Manguera de nivel, atóxica, para líquidos.",
        "full_description": "Manguera de PVC flexible y transparente para visualización de fluidos. Ideal para aplicaciones de nivel, conducción de líquidos a baja presión.",
        "is_active": True,
        "variants": [
            {
                "sku": "MANG-PVC-TR-1/4-M",
                "price": "0.60",
                "stock": 300,
                "attributes": {
                    "Diámetro Interno": "1/4 pulgada",
                    "Color": "Transparente",
                },
                "sort_order": 0,
                "is_active": True,
            },
            {
                "sku": "MANG-PVC-TR-1/2-M",
                "price": "0.90",
                "stock": 200,
                "attributes": {
                    "Diámetro Interno": "1/2 pulgada",
                    "Color": "Transparente",
                },
                "sort_order": 1,
                "is_active": True,
            },
        ],
    },
    {
        "category_name": "Pisos y Revestimientos",
        "name": "Piso de Caucho tipo TACHON (Metro Cuadrado)",
        "slug": "piso-caucho-tachon-m2",
        "short_description": "Piso de caucho con diseño de botones grandes.",
        "full_description": "Similar al piso moneda, pero con un diseño de tachones más grandes. Excelente para rampas y áreas que requieren máximo agarre.",
        "is_active": True,
        "variants": [
            {
                "sku": "PISO-CAU-TACH-NGR-4MM",
                "price": "15.00",
                "stock": 100,
                "attributes": {"Color": "Negro", "Espesor": "4mm"},
                "sort_order": 0,
                "is_active": True,
            },
        ],
    },
]
data.extend(dummy_data)


class Command(BaseCommand):
    help = "Create or update products and their variants in the database."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for entry in data:
            category_name = entry.pop("category_name")
            variants_data = entry.pop("variants", [])

            # 1. Get or create Category
            category_obj, category_created = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": slugify(category_name)},
            )
            if category_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category_obj}"),
                )

            # 2. Create or update Product
            product_lookup = {"name": entry["name"], "category": category_obj}
            product_defaults = {
                k: v for k, v in entry.items() if k not in product_lookup
            }
            product_obj, product_created = Product.objects.update_or_create(
                **product_lookup,
                defaults=product_defaults,
            )
            if product_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created product: {product_obj}"),
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Updated product: {product_obj}"),
                )

            for variant_entry in variants_data:
                attributes_data = variant_entry.pop("attributes", {})

                # 3. Create or update ProductVariant
                variant_lookup = {"sku": variant_entry["sku"]}
                variant_defaults = {
                    k: v for k, v in variant_entry.items() if k not in variant_lookup
                }
                variant_defaults["price"] = Decimal(variant_defaults["price"])
                variant_defaults["product"] = product_obj
                variant_obj, variant_created = ProductVariant.objects.update_or_create(
                    **variant_lookup,
                    defaults=variant_defaults,
                )
                if variant_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"  - Created variant: {variant_obj}"),
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  - Updated variant: {variant_obj}"),
                    )

                for attr_name, attr_value in attributes_data.items():
                    # 4. Get or create Attribute
                    attribute_obj, attribute_created = Attribute.objects.get_or_create(
                        name=attr_name,
                    )
                    if attribute_created:
                        self.stdout.write(
                            self.style.SUCCESS(f"    + Created attribute: {attr_name}"),
                        )

                    # 5. Get or create AttributeValue
                    attribute_value_obj, attribute_value_created = (
                        AttributeValue.objects.get_or_create(
                            attribute=attribute_obj,
                            value=attr_value,
                        )
                    )
                    if attribute_value_created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                (
                                    f"    + Created attribute value: {attr_value} "
                                    f"for attribute: {attr_name}",
                                ),
                            ),
                        )

                    # 6. Link AttributeValue to ProductVariant
                    _, pv_attr_created = (
                        ProductVariantAttributeValue.objects.get_or_create(
                            product_variant=variant_obj,
                            attribute_value=attribute_value_obj,
                        )
                    )
                    if pv_attr_created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                (
                                    f"    + Linked {attr_name}: {attr_value} "
                                    f"to variant {variant_obj.sku}"
                                ),
                            ),
                        )
