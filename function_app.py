# function_app.py

import logging
import io
from PIL import Image
import azure.functions as func

# This creates a new Function App instance.
app = func.FunctionApp()

# This is a "decorator" that registers our function.
# It tells Azure that this function should be triggered by a Blob Storage event.
@app.blob_trigger(arg_name="myblob",
                  path="samples-workitems/{name}", # The container to watch for new files
                  connection="AzureWebJobsStorage")
# This decorator defines the output binding.
# The resized image will be saved to the 'thumbnails' container.
@app.blob_output(arg_name="outputblob",
                 path="thumbnails/{name}", # The container to save thumbnails to
                 connection="AzureWebJobsStorage")
def ImageResize(myblob: func.InputStream, outputblob: func.Out[bytes]):
    logging.info(f"Python blob trigger function processed blob")
    logging.info(f"Name: {myblob.name}")
    logging.info(f"Size: {myblob.length} Bytes")

    try:
        # Read the image data from the input stream
        image_data = myblob.read()
        image = Image.open(io.BytesIO(image_data))

        # Define the size for the thumbnail
        thumbnail_size = (128, 128)
        image.thumbnail(thumbnail_size)

        # Save the resized image to an in-memory byte stream
        output_stream = io.BytesIO()
        # Use the original format or default to PNG
        format = image.format if image.format else 'PNG'
        image.save(output_stream, format=format)
        output_stream.seek(0) # Rewind the stream to the beginning

        # Set the output blob with the thumbnail data
        outputblob.set(output_stream.read())
        logging.info(f"Successfully created thumbnail for {myblob.name}")

    except Exception as e:
        logging.error(f"Error processing image {myblob.name}: {e}")