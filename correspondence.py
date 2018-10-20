import csv

target_file = 'ant'

def corres_package(Metrics, Ref):
    # if 一致しない
    if Metrics == Ref:
        return True
    else:
        return False
        
def corres_class(Metrics, Ref):
    if Metrics == Ref:
        return True
    else:
        return False

def corres_method(Metrics, Ref):
    if Metrics == 'None' or Ref is None:
        return False
    Ref_str = Ref.rstrip('\n').split(' ')[1]
    # Ref_str = Ref_str.rstrip('\n').split(':')
    if Metrics.split(' ')[0] in Ref_str:
        if (Metrics.count(' ') - 1 == Ref[Ref.find(' ')+1:].count(',') and Metrics.split(' ')[1] == ')') or (Metrics.count(' ') - 2 == Ref[Ref.find(' ')+1:].count(',')):
    # if ref[2]とme[1]が一致するもの and ref[3]とme[2]が一致するもの(public, privateを消し，引数の数を見る？可能なら種類も)
            return True
    else:
        return False

def write(target, met='default', flag=0, select=1): #一致度によって0,1,2をつくる
    if select == 1:
        with open('./' + target_file + '/' + target + '.csv', 'a', newline='') as ex:
            writer = csv.writer(ex, delimiter='#')
            met.append(flag)
            writer.writerow(met[4:])
    elif select == 0:
        with open('./' + target_file + '/' + target + '.csv', 'w', newline='') as ex:
            writer = csv.writer(ex, delimiter='#')
            writer.writerow(['class-LOC','class-NOST', 'class-NOACL', 'class-NOAFD', 'class-NOECL',
            'NOFD', 'NOMD', 'NOMF', 'NOPF', 'NOPM',
            'CBO', 'DIT', 'LCOM', 'MAX_CC', 'MAX_LOC', 'MAX_MNON', 'MAX_NOAFD', 'MAX_NOAMD', 'MAX_NOEMD', 'MAX_NOPT', 'MAX_NOST', 'MAX_NOVL',
            'NOAMD', 'NOC', 'NOEMD', 'RFC',
            'method-LOC', 'method-NOST', 'method-NOACL', 'method-NOAFD', 'method-NOECL', 'WMC', 'CC','label'])


def openFile(target):
    if target == 'Extract':
        Extract()


def Extract():
    # open all_refactorings.csv 'r' as ref
    target = 'Extract'
    num = 0 # test
    duplicate_num = 0 
    cfind_num = 0
    write(target, select=0)
    try:
        with open('./ant/all_refactorings.csv', 'r') as ref: 
            next(ref)
            # それぞれ分割
            for line in ref:
                line = line.rstrip('\n').split('#')
        # for all ref[1]
                # if ref[1] == 'Extract Method':
                try:
                    duplication = 0 # test
                    if line[1] == 'Extract Method':
                        # open Metrics.csv as me
                        with open('./'+ target_file + '/csv_data/' + line[0] +  '.csv', 'r') as met: #line[0]
                            next(met)
                            for me in met:
                                me = me.rstrip('\n').split('#')
                                if not corres_package(me[1], line[2][:line[2].rfind('.')]):
                                    #write(target, me, 0)
                                    no_action()
                                elif not corres_class(me[1] + '.' + me[2], line[2]):
                                    write(target, me, 0)
                                elif not corres_method(me[3], line[3]):
                                    if me[3] is not 'None':
                                        write(target, me, 0)
                                else:
                                    write(target, me, 1)
                                    if duplication == 1:
                                        duplicate_num += 1
                                        print('duplicate at {} and sum is {}'.format(line[0], duplicate_num))
                                    duplication = 1
                                    num+=1
                                    # break
                        if duplication == 0:
                            cfind_num += 1
                            print("can't find {} and sum is {}".format(line[0], cfind_num))
                except: #if ファイルが見つからなかったとき
                    print('error at {}'.find(line[0]))
        print(num)

    except:
        print('error')
                    
def no_action():
    return True



if __name__ == '__main__':
    openFile('Extract')
