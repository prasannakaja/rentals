import re
import sys
import optparse
import csv
import urllib.request as urequest

class Trailrentals:
    def __init__(self, infile, csvfile):
        self.postcode_file = infile
        self.URL = "https://www.trailerrentals.com.au/location/near-by?postcode=%s"
        self.tmpfile = open('tempfile.txt', 'w')

        if ".csv" not in csvfile:
            self.csvfile_name = csvfile+".csv"
        else: self.csvfile_name = csvfile


    def write_into_csv(self, location_details_list=[], mode='w'):

        with open(self.csvfile_name, mode, newline='') as csvfile:
            locwriter = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            for loc in location_details_list:
                locwriter.writerow(loc)

    def read_postcodes(self):
        postal_codes = [str(i.strip()) for i in open(self.postcode_file).readlines() if i.strip()]
        return postal_codes

    def scrape_data(self):
        self.write_into_csv()

        postcodes = self.read_postcodes()
        for postcode in postcodes:
            
            self.url = self.URL %postcode
            req = urequest.urlopen(self.url)
            data = req.read()
            loc_list = self.fetch_location(str(data))

            self.write_into_csv(loc_list, mode='a')

    def fetch_location(self, htmldata):
        location_list = []
        name = re.findall(r"<h4>(.*?)</h4>", htmldata)
        address = re.findall(r"<h4>.*?</h4>.*?<span>(.*?)</span>", htmldata)
        state = re.findall(r"<input .*?data-state=\"(.*?)\".*?>", htmldata)
        postal_code = re.findall(r'<input .*?data-postcode=\"(.*?)\".*?>', htmldata)
       
        self.tmpfile.write("%s <> %s\n" %(self.url, len(name)))
        for i, j in enumerate(name):
            location_list.append([name[i], address[i], state[i], postal_code[i]])

        return location_list


def main(options): 
    input_file = options.input_file
    output_filename = options.out_file

    if input_file and output_filename:
        trailObj = Trailrentals(input_file, output_filename)
        trailObj.scrape_data()

    else:
        print(""" Please provide "postcodes text file"  and  
                    "csv file name" to which you want to write output. 

                    script usage is below:

                 python <sciptname> -i<postcode file> -o<name for csv file> 
        """)
        sys.exit(1)
        

if __name__=='__main__':
  
    usage = "usage: program.py -i <postcodes file name> -o <desired csv filename>" 
    parser = optparse.OptionParser(usage=usage) 
    
    parser.add_option('-i', '--input-file',  help="Please provide postcodes.txt file")
    parser.add_option('-o', '--out-file',  help="OUTPUT Filename/provide csv file name")

    (options, args) = parser.parse_args()

    main(options)
    
