from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {"keywords":"Linkedin Headshots","limit":100}   #creating list of arguments
response.download(arguments)   #passing the arguments to the function

