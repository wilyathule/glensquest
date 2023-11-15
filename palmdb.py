# Palm Database File Handler
# based heavily on the information found at https://en.wikipedia.org/wiki/PDB_(Palm_OS)

class PalmDB:
    """Class for handling .pdb files"""

    def __init__(self, filename):
        with open(filename, 'rb') as file:
            self.raw = file.read()
            
            # Parse the header info
            self.header = {
                'raw' : self.raw[0x00:0x4e],
                'name': self.raw[0x00:0x20].decode(),
                'file_attributes': int.from_bytes(self.raw[0x20:0x22], "big"),
                'version': int.from_bytes(self.raw[0x22:0x24], "big"),
                'creation_time': int.from_bytes(self.raw[0x24:0x28], "big"),
                'modification_time': int.from_bytes(self.raw[0x28:0x2c], "big"),
                'backup_time': int.from_bytes(self.raw[0x2c:0x30], "big"),
                'modification_number': int.from_bytes(self.raw[0x30:0x34], "big"),
                'app_info': int.from_bytes(self.raw[0x34:0x38], "big"),
                'sort_info': int.from_bytes(self.raw[0x38:0x3c], "big"),
                'type': int.from_bytes(self.raw[0x3c:0x40], "big"),
                'creator': int.from_bytes(self.raw[0x40:0x44], "big"),
                'unique_id_seed': int.from_bytes(self.raw[0x44:0x48], "big"),
                'next_record_list': int.from_bytes(self.raw[0x48:0x4c], "big"),
                'num_records': int.from_bytes(self.raw[0x4c:0x4e], "big"),
            }
            
            # Parse the record headers
            self.recordheader = []
            
            hdrptr = 0x4e
            
            for i in range(self.header['num_records']):
                self.recordheader.append(
                    {
                        'offset': int.from_bytes(self.raw[hdrptr:hdrptr+4], "big"),
                        'attributes': int.from_bytes(self.raw[hdrptr+4:+hdrptr+5], "big"),
                        'UniqueID': int.from_bytes(self.raw[hdrptr+5:hdrptr+8], "big"),
                    }
                )
                hdrptr += 8

            self.record = []
            
            for i in range(self.header['num_records']):
                if i + 1 < self.header['num_records']:
                    self.record.append(self.raw[self.recordheader[i]['offset']:self.recordheader[i+1]['offset']])
                else:
                    self.record.append(self.raw[self.recordheader[i]['offset']:])
