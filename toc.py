""" Table Of Contents generator for markdown files
    arg[1] = filename to add table of contents to
    arg[2] = indentation (defaults to "  ")
    TODO
        - Create title
        - remove/replace previous toc
"""
import sys

class fileEditor:
    def __init__(self,filepath, indentation="  "):
        self.filepath = filepath
        if indentation == "tab": #indentation pattern
            self.indentation = "\t"
        else:
            self.indentation = indentation
        self.headerList = [] # (string, indentation)
        self.headerListPopulate()
        self.writeToC()
    def headerListPopulate(self):
        """populate the header list from the file's headers"""
        f = open(self.filepath,"r")
        lines=f.readlines()
        disableFlag = False
        for i in lines:
            if "```" in i:
                print("HIT CODEBLOCK")
                disableFlag = not disableFlag
            else:
                if disableFlag == False:
                    indent=0
                    while(i.startswith("#",indent,len(i))):
                        indent=indent+1
                    if indent:
                        headerTitle = self.headerListProcess(i[indent:])
                        self.headerList.append((headerTitle, indent))
        print(self.headerList)

    def headerListProcess(self,inString):
        """process the items in the headerList"""
        inString = inString.strip() #strip whitespace at beginning/end
        linkName = inString #linkName needs no further processing
        inString = inString.lower() #only lowercase

        # replace these characters with nothing
        removeChars = ["(",")","/","."]
        for i in removeChars:
            inString = inString.replace(i,"")

        # replace these characters with dashes
        dashChars = [" "]
        for i in dashChars:
            inString = inString.replace(i,"-")
        return "["+linkName+"](#"+inString+")"

    def writeToC(self):
        """write ToC to file"""
        tocList = []
        for i in self.headerList:
            thisLine ="- "+ i[0]
            c = i[1] - 1
            while c:
                c=c-1
                thisLine = "\t"+thisLine
            thisLine=thisLine+"\n"
            tocList.append(thisLine)

        f = open(self.filepath,"r")
        readlines=f.readlines()
        f.close()

        allLines = tocList+readlines

        f = open(self.filepath+"new","w")
        f.writelines(allLines)
        f.close()

if __name__=="__main__":
    arguments = sys.argv.copy()
    arguments.pop(0)
    filepath = ""
    options = None
    if len(arguments) >= 1:
        filepath = arguments.pop(0)
        if len(arguments) >= 1:
            options = arguments.pop(0)
        fileEditor_i = fileEditor(filepath, options)
    else:
        print("please specify file to create table-of-contents for")
