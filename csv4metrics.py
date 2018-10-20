import csv
from lxml import etree
import glob

FILE_INPUT = ''
target_file = 'ant/data/'
save_csv_file = 'ant/csv_data/'

def parseXML(InputFileName):
    with open(target_file + InputFileName + '.xml', 'rt') as f:
        tree = etree.parse(f)

    with open(save_csv_file + InputFileName + '.csv', 'w', newline='') as cf:
        class_loc = class_nost = class_noacl = class_noafd = class_noecl = 0
        method_loc = method_nost = method_noacl = method_noafd = method_noecl = 0
        
        writer = csv.writer(cf, delimiter="#")
        writer.writerow(
            ['project', 'package', 'class', 'method',
            'class-LOC','class-NOST', 'class-NOACL', 'class-NOAFD', 'class-NOECL',
            'NOFD', 'NOMD', 'NOMF', 'NOPF', 'NOPM',
            'CBO', 'DIT', 'LCOM', 'MAX_CC', 'MAX_LOC', 'MAX_MNON', 'MAX_NOAFD', 'MAX_NOAMD', 'MAX_NOEMD', 'MAX_NOPT', 'MAX_NOST', 'MAX_NOVL',
            'NOAMD', 'NOC', 'NOEMD', 'RFC',
            'method-LOC', 'method-NOST', 'method-NOACL', 'method-NOAFD', 'method-NOECL', 'WMC', 'CC']
            )
        for node in tree.iter():
            if node.tag == 'project':
                project_name = node.attrib.get('name')
                package_name = class_name = method_name = field_name = 'None'
            elif node.tag == 'package':
                package_name = node.attrib.get('name')
                class_name = method_name = field_name = 'None'
            elif node.tag == 'class':
                class_name = node.attrib.get('name')
                method_name = field_name = 'None'
            elif node.tag == 'method':
                method_name = node.attrib.get('name')
                field_name = 'None'
            elif node.tag == 'field':
                field_name = node.attrib.get('name')
                method_name = 'None'
            elif node.tag == 'metrics' and class_name != 'None' and method_name != '.UNKNOWN' and class_name != '.UNKNOWN' and field_name == 'None':
                if method_name == 'None':
                    class_loc = node.attrib.get('LOC')
                    class_nost = node.attrib.get('NOST')
                    class_noacl = node.attrib.get('NOACL')
                    class_noafd = node.attrib.get('NOAFD')
                    class_noecl = node.attrib.get('NOECL')
                    method_loc = method_nost = method_noacl = method_noafd = method_noecl = 0
                elif method_name != 'None':
                    method_loc = node.attrib.get('LOC')
                    method_nost = node.attrib.get('NOST')
                    method_noacl = node.attrib.get('NOACL')
                    method_noafd = node.attrib.get('NOAFD')
                    method_noecl = node.attrib.get('NOECL')

                writer.writerow(
                    [project_name, package_name, class_name, method_name, class_loc, class_nost, class_noacl, class_noafd, class_noecl,
                     node.attrib.get('NOFD'), node.attrib.get('NOMD'),
                     node.attrib.get('NOMF'), node.attrib.get('NOPF'), node.attrib.get('NOPM'), node.attrib.get('CBO'),
                     node.attrib.get('DIT'), node.attrib.get('LCOM'), node.attrib.get('MAX_CC'),
                     node.attrib.get('MAX_LOC'), node.attrib.get('MAX_MNON'),
                     node.attrib.get('MAX_NOAFD'), node.attrib.get('MAX_NOAMD'),node.attrib.get('MAX_NOEMD'), node.attrib.get('MAX_NOPT'),
                     node.attrib.get('MAX_NOST'), node.attrib.get('MAX_NOVL'),
                     node.attrib.get('NOAMD'), node.attrib.get('NOC'), node.attrib.get('NOEMD'), node.attrib.get('RFC'), 
                     method_loc, method_nost, method_noacl, method_noafd, method_noecl,
                     node.attrib.get('WMC'), node.attrib.get('CC')])


            # ['project', 'package', 'class', 'method',
            # 'class-LOC','class-NOST', 'class-NOACL', 'class-NOAFD', 'class-NOECL',
            # 'NOFD', 'NOMD', 'NOMF', 'NOPF', 'NOPM',
            # 'CBO', 'DIT', 'LCOM', 'MAX_CC', 'MAX_LOC', 'MAX_MNON', 'MAX_NOAFD', 'MAX_NOAMD', 'MAX_NOEMD', 'MAX_NOPT', 'MAX_NOST', 'MAX_NOVL',
            # 'NOAMD', 'NOC', 'NOEMD', 'RFC',
            # 'method-LOC', 'method-NOST', 'method-NOACL', 'method-NOAFD', 'method-NOECL', 'WMC', 'CC']

def allFileChangeCSV():
    import os
    num = 0
    try:
        f_n = glob.glob(target_file + '*.xml')
    
    except:
        print("err")
        return False
    
    for f in f_n:
        parseXML(os.path.splitext(f)[0].split('/')[-1])
        num += 1
        print("Done " + str(num) + " files")
    
    print("Done all file")
        #f_p = os.path.splitext(f_n[0])[0]
        #f_p = f_n[0].split('.')[0]        either will do 
        


if __name__ == '__main__':
    allFileChangeCSV()