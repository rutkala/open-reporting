from products.ingestion.extractors.wfs_extractor import WfsExtractor

class PigCbdgExtractor(WfsExtractor):
    def __init__(self):
        super().__init__("pig_cbdg")

if __name__ == '__main__':
    extractor = PigCbdgExtractor()
    extractor.extract_data()
