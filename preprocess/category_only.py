
input_path = "../data/positive_labeled.txt"
output_path = "../data/positive_labeled_category.cor"

class CategoryMaker:
    def __init__(self,txtpath,corpath):
        self.txtPath = txtpath
        self.corPath = corpath
        
        
    def readtxt(self):
        txtfile = open(self.txtPath,"r",encoding='utf-8',errors='ignore')
        lines = txtfile.readlines()
                
        flag = 0
        self.review_list = []
        self.term_list = []
        self.aspect_list = []
        
        review_temp = ""
        term_temp = []
        aspect_temp = []
        
        cnt = 0
        for line in lines:
            if "EOF" in line:
                self.aspect_list.append(aspect_temp)
                break
            if "*****O" in line:
                flag = 1
                if cnt != 0:
                    self.aspect_list.append(aspect_temp)
                    aspect_temp = []
                cnt += 1
                continue
            elif "***T" in line:
                flag = 2
                self.review_list.append(review_temp)
                review_temp = ""
                continue
            elif "***A" in line:
                if flag == 1:
                    self.review_list.append(review_temp)
                    review_temp = ""
                    
                flag = 3
                self.term_list.append(term_temp)
                term_temp = []
                continue
              
            if flag == 1:
                review_temp = line.replace('\n','')
                continue
            if flag == 2:
                term_temp.append(line.replace('\n',''))
                continue
            if flag == 3:
                aspect_temp.append(line.replace('\n',''))
                continue
            
        #print(self.review_list)
        #print('/////////////////////////////////')
        #print(self.term_list)
        #print('/////////////////////////////////')
        #print(self.aspect_list)

              
    def makecor(self):
        final_list = []
        
        for i in range(len(self.review_list)):
            
            num = len(self.aspect_list[i])
            if num == 3:
                final_list.append(self.review_list[i])
                final_list.append(self.aspect_list[i][0])
                final_list.append(self.aspect_list[i][2])
            elif num == 6:
                final_list.append(self.review_list[i])
                final_list.append(self.aspect_list[i][0])
                final_list.append(self.aspect_list[i][2])
                final_list.append(self.review_list[i])
                final_list.append(self.aspect_list[i][3])
                final_list.append(self.aspect_list[i][5])

        f = open(self.corPath, 'w')
        for i in range(len(final_list)):
            f.write(final_list[i])
            f.write('\n')
        f.close()
    
read =CategoryMaker(input_path,output_path)
read.readtxt()
# print(len(read.review_list),len(read.term_list),len(read.aspect_list))
read.makecor()