import marscategory
import marscoordinates 
CUSTOMHANDLERS={"marsapp.categories.field.MarscatField": {'handler_class' : marscategory.CSVMarsCat(), 'file' : False},
                "marsapp.content.schemata.field.CoordinatesField": {'handler_class' : marscoordinates.CSVMarsCoordinates(), 'file' : False},
                }