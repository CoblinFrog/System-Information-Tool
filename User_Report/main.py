from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from computer_info import computer_info

app = FastAPI()

# Point to your templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # Your Python data
    python_data = computer_info
    
    # Return the rendered template with context
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"message": python_data}
    )
