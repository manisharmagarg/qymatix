

class ClarusMappings():

    def mappings(self):

        columns = {
            'Auftragsnr.': 'invoice',
            'Re-/Gu-Datum': 'Date',
            'Artikelnr.': 'product',
            'Artikelgruppennr.': 'product type',
            'Umsatz VK': 'price',
            'Marge': 'margin',
            'Warengruppennr.': 'product line',
            'Menge': 'quantity',
            'MC Kunde': 'account name',
            'Branchennr.': 'product class',
            'Branchenbez.': 'industry',
            'Vertretername': 'kam',
        }

        return columns
    
    def inverted_mappings(self):

        return {v: k for k, v in self.mappings.items()}