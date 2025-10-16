import pandas as pd # type: ignore
import webbrowser
import time 
import requests
from bs4 import BeautifulSoup # type: ignore
import re
import os


df = pd.read_excel(r"C:\Users\Sam\Downloads\Input.xlsx")
# Get all rows
pd.set_option('display.max_rows',None)


# Create a directory to store the text files (optional)
output_dir = "extracted_articles"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    print(f"Processing URL_ID: {url_id}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')  
        
        # Create a string to store all the content
        article_content = ""
        
        # Content inside the 'The Problem' Header 
        problem_header = soup.find('h1', string='The Problem')
        if problem_header:
            all_elements = problem_header.find_all_next()
            problem_texts = []
            for element in all_elements:
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    break
                if element.name == 'p':
                    text_content_problem = element.get_text(strip=True)
                    problem_texts.append(text_content_problem)
                    
            if problem_texts:
                article_content += "THE PROBLEM:\n"
                article_content += '\n'.join(problem_texts) + "\n\n"
        # Content inside the 'Project Objective' Header 

        project_objective_header = soup.find('h1', string='Project Objective')
        if project_objective_header:
            all_elements3 = project_objective_header.find_all_next()
            project_objective_texts = []
            for element3 in all_elements3:
                if element3.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    break
                if element3.name == 'p':
                    text_content_project_objective = element3.get_text(strip=True)
                    project_objective_texts.append(text_content_project_objective)
            if problem_texts:
                article_content += "Project Objective:\n"
                article_content += '\n'.join(project_objective_texts) + "\n\n"  

        
        
        # content inside the 'Project Description' Header
        project_description_header = soup.find('h1', string='Project Description')
        if project_description_header:
            all_elements2 = project_description_header.find_all_next()
            project_description_texts = []
            for element2 in all_elements2:
                if element2.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    break
                if element2.name == 'p':
                    text_content_project_description = element2.get_text(strip=True)
                    project_description_texts.append(text_content_project_description)
                    
            if problem_texts:
                article_content += "Project Description:\n"
                article_content += '\n'.join(project_description_texts) + "\n\n"        
        
        
        # content inside the 'Our Solution' Header
        solution_header = soup.find('h1', string='Our Solution')
        if solution_header:
            all_elements1 = solution_header.find_all_next()
            solution_texts = []
            for element1 in all_elements1:
                if element1.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    break
                if element1.name == 'p':
                    text_content_solution = element1.get_text(strip=True)
                    solution_texts.append(text_content_solution)
                    
            if solution_texts:
                article_content += "OUR SOLUTION:\n"
                article_content += '\n'.join(solution_texts) + "\n\n"
        
        # content inside the 'Project Deliverables' Header
        project_deliverables_header = soup.find('h1', string='Project Deliverables')
        if project_deliverables_header:
            all_elements4 = project_deliverables_header.find_all_next()
            project_deliverables_texts = []
            for element4 in all_elements4:
                if element4.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    break
                if element4.name == 'p':
                    text_content_project_deliverables = element4.get_text(strip=True)
                    project_deliverables_texts.append(text_content_project_deliverables)
                    
            if solution_texts:
                article_content += "OUR SOLUTION:\n"
                article_content += '\n'.join(solution_texts) + "\n\n"


        
        # content inside the 'Client Background' Header
        p_tags = soup.find_all('p')
        client_found = False
        industry_found = False
        product_and_services = False
        organization_size = False
        
        article_content += "CLIENT BACKGROUND:\n"
        for p in p_tags:
            text_content = p.get_text(strip=True)      
            if 'Client:' in text_content and not client_found:
                article_content += text_content + "\n"
                client_found = True
            if 'Industry Type:' in text_content and not industry_found:
                article_content += text_content + "\n"
                industry_found = True
            if 'Products & Services:' in text_content and not product_and_services:
                article_content += text_content + "\n"
                product_and_services = True
            if 'Organization Size:' in text_content and not organization_size:
                article_content += text_content + "\n"
                organization_size = True
        article_content += "\n"
        
        # content inside the 'Deliverables' Header
        deliverables_header = soup.find('h1', string='Deliverables')                  
        if deliverables_header:
            next_p_deliverables = deliverables_header.find_next_siblings('p')
            deliverables = []
            
            for p in next_p_deliverables:
                text_content = p.get_text(strip=True)
                
                # Stop conditions
                if any(stop_phrase in text_content.lower() for stop_phrase in 
                       ['http', 'www.', 'blackcoffer', 'contact', 'summarized', 'project was done']):
                    break
                    
                deliverables.append(text_content)
            
            # Add deliverables to content
            article_content += "DELIVERABLES:\n"
            for item in deliverables:
                article_content += f"• {item}\n"
            article_content += "\n"
        
        # content inside the 'Tech Stack' Header
        tech_stack = soup.find(class_='wp-block-list')
        if tech_stack:
            article_content += "TECH STACK:\n"
            list_items = tech_stack.find_all('li')
            for item in list_items:
                tech_used = item.get_text(strip=True)
                article_content += f"• {tech_used}\n"
            article_content += "\n"
        
        # Save to text file with URL_ID as filename
        filename = f"{url_id}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(article_content)
        
        print(f"Article saved to: {filepath}")
        print(f"{'='*60}\n")
    
    except Exception as e:
        print(f"Error processing URL_ID {url_id}: {e}")
        continue

print("All articles extracted and saved successfully!")