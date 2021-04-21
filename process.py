#Spazer tool for processing web pages
#DCBD Assignment 1
#Arpan Biswas (MDS202011), Chandrashish Prasad (MDS202015), Megha Chakraborty (MDS202022)

from bs4 import BeautifulSoup
import pathlib

space_gained = 0
space_input = 0
for x in range(10):
    filename = str(x) + ".html"
    file = pathlib.Path('input/' + filename)
    if (file.exists()):
        #Read each file
        f = open('input/' + filename, 'r', errors="ignore")
        contents = f.read()   
        
        #Remove html tags
        soup = BeautifulSoup(contents, 'lxml')
        
        #Check for Address tags
        address_tag_found = False
        address_lines = []
        for element in soup.find_all(["address"]):
            address_tag_found = True
            address_lines.append(element.get_text())
            element.decompose()
        
        #Check for Address class or ID
        for element in soup.find_all():
            if element.attrs:
                name = ""
                if element.has_attr("class"):
                    name += " ".join(element["class"]).lower()
                if element.has_attr("id"):
                    name += (" " if name else "") + element["id"].lower()
                if name:
                    if ("address" in name) and ("email" not in name):
                        address_tag_found = True
                        address_lines.append(element.get_text())
                        element.decompose()
                    if ("phone" in name) or ("email" in name):
                        address_lines.append(element.get_text())

        if address_tag_found:
            text = "\n".join(address_lines)
        else:
            #Remove Scripts, Styles, Headings, Meta and Images (SAFE)
            for element in soup.find_all(["script", "style", "head", "meta", "title", "h1", "h2", "h3", "h4", "h5", "h6", "img"]):
                element.decompose()
            
            #Remove elements that might be heading or menu (CAUTION)
            for element in soup.find_all():
                if element.attrs:
                    name = ""
                    if element.has_attr("class"):
                        name += " ".join(element["class"]).lower()
                    if element.has_attr("id"):
                        name += (" " if name else "") + element["id"].lower()
                    if name:
                        if ("menu" in name) or ("heading" in name):
                            element.decompose()
            
            text = soup.get_text()
        
        #Remove unnecessary spaces and newlines (SAFE)
        lines = [line.strip() for line in text.splitlines()]
        lines = [" ".join(line.split()) for line in lines if line]
        
        #Remove chunks of text in long lines that are not close to any comma (CAUTION)
        for i in range(len(lines)):
            parts = lines[i].split(",")
            for j in range(len(parts)):
                p = parts[j]
                if len(p) > 150:
                    parts[j] = p[0:75]+p[-75:]
            lines[i] = ",".join(parts)
        output = "\n".join(lines)

        #Write the output variable contents to output/ folder.
        fw = open('output/' + filename, "w")
        fw.write(output)
        fw.close()
        f.close()
        
        #Calculate space savings
        space_input = space_input + len(contents)
        space_gained = space_gained + len(contents) - len(output)

print("Total Space Gained = " + str(round(space_gained*100/space_input, 2)) + "%")
