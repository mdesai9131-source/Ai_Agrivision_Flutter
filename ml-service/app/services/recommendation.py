from typing import Dict, Any, Optional
from app.schemas.prediction_schema import RecommendationData

# Comprehensive agricultural knowledge base for crop diseases
DISEASE_RECOMMENDATION_DATABASE: Dict[str, Dict[str, Any]] = {
    "Tomato___Early_Blight": {
        "disease": "Tomato Early Blight (Alternaria solani)",
        "description": "A common fungal disease affecting tomato foliage, stems, and fruits, characterized by concentric dark ring patterns on older leaves.",
        "symptoms": [
            "Small brown-to-black spots appearing initially on older/lower leaves",
            "Target-board concentric rings developing within the spots",
            "Yellow halo surrounding leaf lesions causing premature leaf drop",
            "Collar rot lesions at soil level on stems in young transplants"
        ],
        "prevention": [
            "Practice 2-3 year crop rotation with non-solanaceous crops",
            "Use drip or furrow irrigation to keep foliage dry rather than overhead watering",
            "Ensure proper plant spacing (45-60 cm) to promote air circulation",
            "Apply organic mulch around plant bases to prevent soil splash onto lower foliage",
            "Remove and destroy infected lower leaves early in the season"
        ],
        "management": [
            "Prune infected bottom leaves during dry morning weather using sanitized shears",
            "Stake and cage plants to keep foliage elevated away from wet soil",
            "If biological or organic treatments are desired, consider copper fungicides or Bacillus subtilis according to official instructions",
            "Note on Chemical Controls: Follow local agriculture extension guidelines. Always read authorized product packaging for application rates and pre-harvest intervals. Never use unregistered chemicals."
        ],
        "expert_required": False
    },
    "Tomato___Late_Blight": {
        "disease": "Tomato Late Blight (Phytophthora infestans)",
        "description": "A highly destructive water mold disease capable of devastating tomato and potato crops within days during cool, wet conditions.",
        "symptoms": [
            "Irregular water-soaked greasy brown lesions on leaves and stems",
            "White, downy fungal-like growth on the undersides of leaves in humid weather",
            "Dark, firm, sunken rot on green or ripe fruits",
            "Rapid collapse and browning of entire foliage branches"
        ],
        "prevention": [
            "Plant certified disease-free transplants and resistant cultivars",
            "Avoid planting adjacent to potato fields or volunteer potatoes",
            "Eliminate all cull piles and volunteer tomato/potato plants immediately",
            "Monitor weather forecasts for prolonged cool (15-22°C) and high humidity conditions"
        ],
        "management": [
            "Immediately isolate and destroy heavily infected plants in bags (do not compost)",
            "Cease overhead irrigation instantly",
            "Consult local agricultural extension officers or certified agronomists immediately for community outbreak management and authorized systemic protections."
        ],
        "expert_required": True
    },
    "Tomato___Bacterial_spot": {
        "disease": "Tomato Bacterial Spot (Xanthomonas spp.)",
        "description": "A bacterial infection causing foliar lesions and fruit scabbing, prevalent during warm, rainy periods.",
        "symptoms": [
            "Small, dark, water-soaked circular lesions on leaves",
            "Leaves turn yellow and drop, exposing developing fruits to sunscald",
            "Rough, scabby raised brown spots on green tomato fruits"
        ],
        "prevention": [
            "Use hot-water treated or certified disease-free seeds",
            "Disinfect greenhouse benches, stakes, and pruning tools regularly",
            "Avoid working in tomato fields when leaves are wet to halt bacterial transmission",
            "Rotate crops with non-host species for at least 2 seasons"
        ],
        "management": [
            "Remove initial localized diseased leaves if spotted early",
            "Apply registered fixed copper bactericides if recommended by regional agricultural advisories",
            "Consult an agro-expert if widespread fruit scabbing occurs."
        ],
        "expert_required": False
    },
    "Tomato___Leaf_Mold": {
        "disease": "Tomato Leaf Mold (Passalora fulva)",
        "description": "Fungal condition predominantly occurring in greenhouse and high-tunnel tomatoes with poor ventilation and high humidity.",
        "symptoms": [
            "Pale greenish-yellow spots on the upper leaf surfaces",
            "Olive green to brownish velvety mold growth on the corresponding undersurface",
            "Wilted and curled leaves falling prematurely"
        ],
        "prevention": [
            "Maximize greenhouse ventilation using fans and side louvers",
            "Maintain relative humidity below 85%",
            "Space plants generously to ensure ample light and airflow",
            "Warm up greenhouses before sunrise to prevent dew formation"
        ],
        "management": [
            "Prune lower foliage to facilitate under-canopy air movement",
            "Sanitize greenhouse structure thoroughly between crop cycles",
            "Use biofungicides labeled for greenhouse tomatoes under expert guidance"
        ],
        "expert_required": False
    },
    "Tomato___Yellow_Leaf_Curl_Virus": {
        "disease": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "description": "A devastating viral disease transmitted by the silverleaf whitefly (Bemisia tabaci), causing stunted growth and cupped leaves.",
        "symptoms": [
            "Severe upward curling and cupping of leaflet margins",
            "Distinct yellowing (chlorosis) along leaf veins and edges",
            "Extreme plant stunting and bushy erect appearance",
            "Dramatic flower drop and failure to set fruit"
        ],
        "prevention": [
            "Use TYLCV-resistant or tolerant tomato hybrids",
            "Deploy yellow sticky traps inside fields and greenhouses to monitor whitefly vectors",
            "Use insect-proof netting (50 mesh) in nursery seedling houses",
            "Maintain weed-free field borders to eliminate alternate whitefly hosts"
        ],
        "management": [
            "Rogue and bury or burn infected plants immediately to prevent vector spread",
            "Adopt integrated pest management (IPM) for whitefly control using horticultural oils or neem extracts",
            "Contact your nearest agricultural department for district-level whitefly containment alerts."
        ],
        "expert_required": True
    },
    "Tomato___Healthy": {
        "disease": "Healthy Tomato",
        "description": "The crop foliage exhibits vibrant green color, uniform texture, and no detectable signs of fungal, bacterial, or viral stress.",
        "symptoms": [
            "Uniform leaf coloration without chlorosis, necrosis, or spotting",
            "Firm, upright stems and vigorous vegetative growth"
        ],
        "prevention": [
            "Maintain balanced N-P-K fertilization and regular calcium supply to prevent blossom-end rot",
            "Consistent moisture management via scheduled drip irrigation",
            "Routine weekly scouting for early signs of pests or lesions"
        ],
        "management": [
            "Continue optimal agronomic practices",
            "Keep records of planting dates and growth cycles"
        ],
        "expert_required": False
    },
    "Potato___Early_Blight": {
        "disease": "Potato Early Blight (Alternaria solani)",
        "description": "Fungal foliage and tuber disease causing circular concentric lesions and premature defoliation in potato fields.",
        "symptoms": [
            "Dark brown spots with concentric ring patterns on older foliage",
            "Yellowing around lesions, progressing upward along the stem",
            "Dark, dry, sunken corky lesions on potato tubers"
        ],
        "prevention": [
            "Plant certified disease-free seed tubers",
            "Provide balanced nitrogen nutrition; avoid crop stress during tuber bulking",
            "Practice 3-year crop rotation avoiding other nightshade crops"
        ],
        "management": [
            "Ensure regular irrigation during dry spells to prevent plant stress",
            "Destroy diseased vine residues after harvest",
            "Consult local agronomic extension regarding registered foliar fungicides if disease threshold is crossed."
        ],
        "expert_required": False
    },
    "Potato___Late_Blight": {
        "disease": "Potato Late Blight (Phytophthora infestans)",
        "description": "Historically devastating oomycete that triggers rapid foliage blight and tuber rotting under moist, cool conditions.",
        "symptoms": [
            "Dark brown-black water-soaked lesions spreading rapidly from leaf tips",
            "Delicate white fungal mold on leaf undersides in morning dew",
            "Brownish dry granular rot penetrating beneath the skin of tubers"
        ],
        "prevention": [
            "Plant certified resistant seed potatoes",
            "Eliminate potato cull piles and volunteer sprouts before planting season",
            "Hilling up soil deeply to protect developing tubers from spore wash-off"
        ],
        "management": [
            "Kill potato vines before harvest if blight is active to prevent tuber contamination",
            "Allow tubers to cure properly before storage and maintain cool, ventilated storage",
            "Notify your local agricultural extension service immediately if late blight is detected."
        ],
        "expert_required": True
    },
    "Potato___Healthy": {
        "disease": "Healthy Potato",
        "description": "The potato canopy exhibits vigorous, uniform foliage with healthy coloration and healthy vegetative growth.",
        "symptoms": [
            "Clean green foliage without spotting or wilting",
            "Strong turgid leaf stems and healthy root canopy"
        ],
        "prevention": [
            "Maintain adequate hilling and soil moisture",
            "Monitor soil fertility and scout regularly for aphids or beetles"
        ],
        "management": [
            "Continue standard crop stewardship"
        ],
        "expert_required": False
    },
    "Corn___Common_rust": {
        "disease": "Corn Common Rust (Puccinia sorghi)",
        "description": "Fungal rust disease characterized by reddish-brown pustules on both upper and lower corn leaf surfaces.",
        "symptoms": [
            "Small powdery cinnamon-brown pustules scattered across both leaf surfaces",
            "Pustules rupture epidermal tissue, turning dark brown to black as the plant matures",
            "Severe infections cause leaf yellowing and premature desiccation"
        ],
        "prevention": [
            "Plant resistant corn hybrids adapted to your agro-climatic zone",
            "Early planting can help crops advance past susceptible growth stages before rust spores arrive"
        ],
        "management": [
            "Monitor lower leaves; treatment is rarely required unless rust reaches ear leaf during early pollination",
            "Consult regional crop agronomist if pustules spread aggressively prior to tasseling."
        ],
        "expert_required": False
    },
    "Corn___Northern_Leaf_Blight": {
        "disease": "Corn Northern Leaf Blight (Exserohilum turcicum)",
        "description": "Foliar disease producing characteristic cigar-shaped grayish-green lesions on corn leaves.",
        "symptoms": [
            "Elongated, elliptical cigar-shaped lesions (2.5 to 15 cm long)",
            "Lesions appear grayish-green, turning tan with dark spore bands",
            "Extensive leaf blighting reducing photosynthetic capacity"
        ],
        "prevention": [
            "Select resistant hybrids with high tolerance ratings",
            "Rotate with non-host crops such as soybean, alfalfa, or small grains",
            "Manage crop residue to encourage decomposition of overwintering fungi"
        ],
        "management": [
            "Scout weekly from vegetative stages through silking",
            "Seek guidance from agricultural extension regarding registered treatments if upper canopy is threatened before milk stage."
        ],
        "expert_required": False
    },
    "Corn___Healthy": {
        "disease": "Healthy Corn / Maize",
        "description": "Strong, erect stalks with vibrant green lanceolate leaves and healthy silk/ear development.",
        "symptoms": [
            "Even green coloration throughout the canopy",
            "Robust stalk and healthy brace roots"
        ],
        "prevention": [
            "Provide optimal nitrogen scheduling and weed control",
            "Maintain soil drainage to prevent root waterlogging"
        ],
        "management": [
            "Continue standard agronomic practices"
        ],
        "expert_required": False
    },
    "Wheat___Brown_Rust": {
        "disease": "Wheat Brown Rust / Leaf Rust (Puccinia triticina)",
        "description": "A prevalent fungal rust disease that attacks wheat foliage, producing scattered reddish-orange to brown pustules on leaf blades.",
        "symptoms": [
            "Small, circular to oval, reddish-brown pustules scattered erratically across the upper leaf surface",
            "Yellowing (chlorosis) around dense clusters of pustules",
            "Powdery rust spores rubbing off easily when brushed with fingers",
            "Premature desiccation of flag leaves, directly reducing grain fill and yield"
        ],
        "prevention": [
            "Sow certified rust-resistant wheat varieties recommended for your agro-ecological zone",
            "Avoid excessive early-season nitrogen fertilization, which creates dense lush canopies prone to spore germination",
            "Maintain recommended seed rates to encourage inter-row air circulation and fast leaf drying",
            "Eradicate volunteer wheat plants during the off-season to break the green bridge cycle"
        ],
        "management": [
            "Regularly scout the field, especially flag leaves during boot and heading stages",
            "If rust pustules are detected before heading on susceptible varieties, consult your local Krishi Vigyan Kendra (KVK) or agricultural extension officer for approved triazole or strobilurin fungicide recommendations",
            "Follow official label directions strictly for pre-harvest intervals and spray volumes"
        ],
        "expert_required": True
    },
    "Wheat___Yellow_Rust": {
        "disease": "Wheat Yellow Rust / Stripe Rust (Puccinia striiformis)",
        "description": "A devastating airborne rust disease prevalent in cool, humid wheat-growing regions, forming distinct yellow pustules in narrow stripes.",
        "symptoms": [
            "Bright yellow to orange-yellow powdery pustules arranged in narrow, parallel linear stripes along leaf veins",
            "Stripe patterns giving a beaded appearance along mature leaves",
            "Chlorotic yellow patches followed by tissue necrosis and browning",
            "In severe attacks, pustules can spread to leaf sheaths and glumes/ears"
        ],
        "prevention": [
            "Plant newly released, genetically resistant cultivars (avoid repeating obsolete susceptible varieties)",
            "Plant at recommended timely sowing dates (avoid late sowing which exposes crops to spore clouds)",
            "Balance soil fertilization with adequate potassium to bolster cell wall resistance"
        ],
        "management": [
            "Immediately notify local agricultural extension officers upon observing yellow stripe foci in your fields",
            "In cool (10-15°C) humid weather, apply university/KVK recommended fungicides promptly when disease reaches economic threshold",
            "Ensure full coverage of upper leaves (Flag leaf and Flag-1 leaf) using calibrated sprayers"
        ],
        "expert_required": True
    },
    "Wheat___Powdery_Mildew": {
        "disease": "Wheat Powdery Mildew (Blumeria graminis f. sp. tritici)",
        "description": "A fungal disease causing white-to-gray powdery patches on the lower leaf surface, progressing upward in dense, humid crop stands.",
        "symptoms": [
            "Fluffy, white to gray powdery fungal patches predominantly on lower leaves and stems",
            "Patches gradually turn grayish-brown with tiny black dots (cleistothecia) late in the season",
            "Leaf tissue underneath turns chlorotic and dies prematurely",
            "Stunted tillers and reduced grain test weight"
        ],
        "prevention": [
            "Avoid overly dense plant populations and ensure optimal row spacing",
            "Avoid excessive nitrogenous fertilizer application",
            "Rotate crops and avoid continuous wheat-on-wheat cropping"
        ],
        "management": [
            "Scout lower leaves starting at tillering stage",
            "Consult regional agriculture experts for registered foliar treatments if mildew spreads past the lower canopy before heading"
        ],
        "expert_required": False
    },
    "Wheat___Septoria": {
        "disease": "Wheat Septoria Leaf Blotch (Zymoseptoria tritici)",
        "description": "A destructive foliar disease causing irregular necrotic blotches peppered with tiny black fruiting bodies.",
        "symptoms": [
            "Irregular, elongated tan-to-brown necrotic blotches bounded by leaf veins",
            "Distinct tiny black specks (pycnidia) embedded inside the dead lesions (visible under hand lens)",
            "Yellowing surrounding lesions leading to rapid canopy dry-down"
        ],
        "prevention": [
            "Select wheat varieties with proven tolerance to Septoria tritici",
            "Practice deep incorporation of wheat stubble to reduce overwintering fungal inoculum",
            "Implement a minimum 2-year crop rotation with non-cereal crops"
        ],
        "management": [
            "Scout during stem elongation through flag leaf emergence",
            "Apply approved protective fungicides if prolonged rainy weather coincides with flag leaf emergence, per extension advice"
        ],
        "expert_required": False
    },
    "Wheat___Healthy": {
        "disease": "Healthy Wheat",
        "description": "The wheat crop exhibits healthy, erect foliage with vibrant green coloration and no visible signs of rust pustules, blights, or mildew.",
        "symptoms": [
            "Clean, linear green leaf blades without pustules, chlorosis, or necrotic spotting",
            "Sturdy tillers and healthy vegetative growth"
        ],
        "prevention": [
            "Maintain timely irrigation at critical growth stages (Crown Root Initiation, Tillering, Booting, Heading, Milking)",
            "Ensure balanced N-P-K and micronutrient (Zinc, Iron) management based on soil testing",
            "Continue weekly field walks to scout for early airborne rust arrivals"
        ],
        "management": [
            "Continue recommended agronomic stewardship practices",
            "Maintain field cleanliness and adequate drainage"
        ],
        "expert_required": False
    },
    "Rice___Brown_Spot": {
        "disease": "Rice Brown Spot (Bipolaris oryzae)",
        "description": "A fungal disease causing circular to oval brown spots with yellow halos across rice leaves, commonly associated with nutrient-deficient soils.",
        "symptoms": [
            "Small circular to oval brown spots scattered across leaves",
            "Older lesions have gray or whitish centers with dark brown margins and yellow halos",
            "In severe cases, lesions coalesce causing leaf drying and reduced grain filling"
        ],
        "prevention": [
            "Ensure balanced soil fertility; avoid potassium and silicon deficiency",
            "Treat seeds with hot water or certified biological seed treatments prior to sowing",
            "Maintain proper water management and avoid extreme drying of paddy fields"
        ],
        "management": [
            "Apply recommended fertilizer top-dressing (especially potassium) to alleviate plant nutritional stress",
            "Consult local agro-extension officers for registered organic or chemical foliar interventions if damage exceeds economic threshold"
        ],
        "expert_required": False
    },
    "Rice___Leaf_Blast": {
        "disease": "Rice Leaf Blast (Magnaporthe oryzae)",
        "description": "One of the most destructive diseases of cultivated rice, producing characteristic spindle-shaped lesions that can kill entire seedlings.",
        "symptoms": [
            "Diamond-shaped or spindle-shaped lesions with gray-white centers and brown or reddish-brown borders",
            "Lesions enlarge rapidly and coalesce, causing entire leaves to scorch and wither",
            "In severe cases, blast reaches node and neck ('Neck Blast'), causing empty, bleached panicles"
        ],
        "prevention": [
            "Use blast-resistant certified paddy varieties recommended for your region",
            "Avoid high dosages of nitrogen fertilizer, especially in split applications during overcast, humid periods",
            "Maintain continuous shallow water depth in the field during vegetative stage"
        ],
        "management": [
            "Immediately reduce top-dress nitrogen if blast symptoms are spotted",
            "Consult agricultural authorities / KVK immediately for area-wide blast warnings and recommended systemic treatments"
        ],
        "expert_required": True
    },
    "Rice___Healthy": {
        "disease": "Healthy Rice / Paddy",
        "description": "Vibrant green upright rice tillers with clean leaf blades, robust root systems, and uniform growth.",
        "symptoms": [
            "Clean, deep-green linear blades without spots, lesions, or leaf tip necrosis",
            "Uniform tiller development and healthy panicle emergence"
        ],
        "prevention": [
            "Maintain optimal water management and system of rice intensification (SRI) guidelines where applicable",
            "Conduct routine leaf color chart (LCC) monitoring for precision nitrogen application"
        ],
        "management": [
            "Continue standard paddy management protocols"
        ],
        "expert_required": False
    },
    "Wheat___Brown_Rust": {
        "disease": "Wheat Brown Rust / Leaf Rust (Puccinia triticina)",
        "description": "Fungal disease characterized by scattered reddish-orange to brown pustules primarily on the upper surfaces of wheat leaf blades.",
        "symptoms": [
            "Small, circular to oval orange-brown powdery pustules scattered randomly across leaf blades",
            "Pustules rupture the leaf epidermis, turning dark brown as the plant approaches maturity",
            "Early leaf senescence causing shriveled grain and significant yield reduction"
        ],
        "prevention": [
            "Sow certified rust-resistant wheat varieties recommended for your agro-climatic zone",
            "Ensure timely sowing during the recommended planting window to avoid peak spore exposure",
            "Avoid excessive nitrogen fertilization which produces dense, susceptible vegetative canopy",
            "Eradicate volunteer wheat plants and alternative weed hosts around field margins"
        ],
        "management": [
            "Scout wheat fields weekly from tillering through grain filling stages",
            "If pustules appear on flag leaves prior to heading, contact your local KVK or extension agronomist",
            "Apply approved biocontrol agents or regional agricultural university recommended protective sprays adhering strictly to pre-harvest intervals"
        ],
        "expert_required": True
    },
    "Wheat___Yellow_Rust": {
        "disease": "Wheat Stripe Rust / Yellow Rust (Puccinia striiformis)",
        "description": "High-impact fungal rust prevalent in cooler temperatures, forming distinct bright yellow parallel pustule stripes along leaf veins.",
        "symptoms": [
            "Bright yellow to orange pustules arranged in prominent parallel stripes or linear rows along leaf veins",
            "Chlorotic yellow stripes advancing rapidly from leaf tip to base under cool, dewy conditions",
            "Severe infections attack the glumes and awns, leaving dusty yellow spore masses"
        ],
        "prevention": [
            "Plant yellow rust resistant or tolerant wheat varieties (e.g., HD-2967, DBW series as recommended by ICAR/CIMMYT)",
            "Adopt crop rotation and avoid planting continuous wheat across wide contiguous tracts",
            "Monitor regional meteorological alerts for cool (10-15°C) humid spells favoring rust development"
        ],
        "management": [
            "Mark and isolate initial yellow rust focal spots immediately upon detection",
            "Consult local agricultural department officers promptly for district-wide stripe rust containment",
            "Follow official package of practices for authorized triazole or strobilurin protective measures if economic threshold is exceeded"
        ],
        "expert_required": True
    },
    "Wheat___Powdery_Mildew": {
        "disease": "Wheat Powdery Mildew (Blumeria graminis f. sp. tritici)",
        "description": "Fungal disease causing fluffy white to light gray powdery colonies on leaves, stems, and heads during humid, shaded conditions.",
        "symptoms": [
            "White to grayish powdery fungal patches on the upper surface of lower leaves and leaf sheaths",
            "Patches coalesce covering entire leaves, turning dull gray-brown with tiny black fruiting bodies (cleistothecia)",
            "Premature yellowing and drying of lower foliage"
        ],
        "prevention": [
            "Select resistant cultivars with proven adult-plant resistance",
            "Avoid excessively high seeding density to ensure ample sunlight and air penetration into lower canopy",
            "Balanced fertilizer application; avoid over-application of nitrogen"
        ],
        "management": [
            "Improve field aeration and drainage",
            "Scout canopy weekly to prevent upward movement onto the critical flag leaf",
            "Consult agricultural extension advisors for biological or targeted sulfur/fungicidal options if infection reaches the middle canopy before heading"
        ],
        "expert_required": False
    },
    "Wheat___Septoria": {
        "disease": "Wheat Septoria Leaf Blotch (Zymoseptoria tritici / Septoria nodorum)",
        "description": "Foliar disease initiating as yellow flecks that expand into irregular tan-brown necrotic blotches speckled with tiny black pycnidia.",
        "symptoms": [
            "Irregular oval or elongated tan to grayish-brown necrotic lesions bounded by leaf veins",
            "Characteristic tiny black speck-like fruiting bodies (pycnidia) embedded inside older lesions",
            "Extensive foliar blight causing scorched leaf appearance and premature desiccation"
        ],
        "prevention": [
            "Use certified clean, fungicide-treated seed",
            "Incorporate or decompose wheat stubble to eliminate primary overwintering inoculum",
            "Practice 2-year crop rotation with non-cereal crops like pulses, mustard, or chickpeas"
        ],
        "management": [
            "Scout lower leaves after rain events during stem elongation (Zadoks GS 31-39)",
            "Preserve the top two leaf tiers (flag leaf and leaf 2) through timely crop stewardship",
            "Consult local extension services for integrated disease management and approved foliar protection"
        ],
        "expert_required": False
    },
    "Wheat___Healthy": {
        "disease": "Healthy Wheat",
        "description": "The wheat canopy displays uniform emerald-green coloration, upright tillers, and healthy flag leaves free of biotic lesions or rust pustules.",
        "symptoms": [
            "Vibrant, uniform green leaf blades without chlorotic stripes, rust pustules, or blotches",
            "Sturdy tillering, clean leaf sheaths, and vigorous vegetative development"
        ],
        "prevention": [
            "Maintain balanced N-P-K nutrition with micronutrient zinc supplementation if indicated by soil test",
            "Schedule irrigations at critical growth stages: Crown Root Initiation (CRI), tillering, flowering, and grain filling",
            "Routine weekly field scouting for early pest or rust detection"
        ],
        "management": [
            "Continue standard good agricultural practices (GAP)",
            "Maintain optimal weed and irrigation stewardship"
        ],
        "expert_required": False
    }
}

class RecommendationService:
    @staticmethod
    def get_recommendation(crop: Optional[str], disease: Optional[str]) -> Optional[RecommendationData]:
        """
        Retrieves safe agricultural guidance matching crop and disease.
        Strictly forbids unauthorized chemical dosages.
        """
        if not crop or not disease:
            return None

        # Build lookup key
        sanitized_crop = crop.replace(" ", "_").strip()
        sanitized_disease = disease.replace(" ", "_").strip()
        key = f"{sanitized_crop}___{sanitized_disease}"

        # Direct match or partial match
        match = DISEASE_RECOMMENDATION_DATABASE.get(key)

        if not match:
            # Fallback search by disease substring
            for k, val in DISEASE_RECOMMENDATION_DATABASE.items():
                if sanitized_crop.lower() in k.lower() and sanitized_disease.lower() in k.lower():
                    match = val
                    break

        if not match:
            # Generic safe advisory
            if "healthy" in disease.lower():
                return RecommendationData(
                    disease=f"Healthy {crop}",
                    description=f"The {crop} plant appears healthy with no conspicuous symptoms of biotic pathogen stress.",
                    symptoms=["Normal leaf texture, vibrant color, and standard growth rate."],
                    prevention=["Maintain regular crop scouting, balanced soil nutrition, and clean irrigation."],
                    management=["Continue current crop management routines."],
                    expert_required=False
                )
            else:
                return RecommendationData(
                    disease=f"{crop} {disease}",
                    description=f"Pathological signs detected on {crop} leaf consistent with {disease}.",
                    symptoms=["Foliar discoloration or tissue necrosis consistent with disease manifestation."],
                    prevention=[
                        "Ensure clean cultural practices and sanitize tools between rows.",
                        "Inspect surrounding crops to assess whether the issue is isolated or spreading.",
                        "Avoid overhead irrigation to minimize leaf wetness."
                    ],
                    management=[
                        "Remove visibly decaying or blighted foliage and dispose away from the field.",
                        "Safety Note: Do not apply unverified chemical mixtures. For certified chemical/biological treatments, consult your local agricultural extension service or certified crop advisor."
                    ],
                    expert_required=True
                )

        return RecommendationData(**match)

recommendation_service = RecommendationService()
