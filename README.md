# Smile-Classifier

This is a **Smile Classifier** website. It contains 3 web pages, 
<ol>
<li> Home - Describes the functionality and technical matters of the website </li>
<li> Classify Image - This page takes an image as input through a form to classify it as "Smiling" or "Not-Smiling" </li>
<li> Classification History - This page shows the all images that has been uploaded to classify along with the predicted class and upload time.</li>
</ol>

## How to use this website
You can read the paragraph in "Home" page which describes how this website works but this is not mandatory. For classifying an image go to the classify image page by clicking "Classify Image" in the nav bar. Then upload an image and hit the "Classify" button. After that the classification result will shown along with the uploaded image in the same page, below the section where image was uploaded. Also, it stores the result and image for updating the entries in history page. In "Classification History" page you can see the all uploaded images till the time along with their predicted class and upload time for each.

## How to install in your local device
` git clone <Clone url link> ` 

Then go to the folder and open it using VScode. Then open command prompt in VScode and run - `pip install -r requirements.txt`

Now run `cd app`
Then run `uvicorn main:app --reload`

**N.B: Don't forget to install MySQL in your local machine and modify database.py file according to your MySQL workbench configuration.**

## Tech Stack Used

<ul>
  <li> <b>Front-End: HTML and CSS</b> </li>
  <li> <b>Back-End: FastAPI and Python</b> </li>
  <li> <b>Server-Side: My-SQL (Database) and SQLAlchemy (ORM)</b> </li>
</ul>

## Recorded Preview

https://github.com/user-attachments/assets/fdbced2a-4da7-4f32-aeda-e77272e9d8e8

