# importamos al framework fastapi a nuestro entorno de trabajo
# Importamos la libreria pydantic para manejar los datos y pandas para manejar los datos en formato de tabla
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd

# Creamos un objeto apartir de la clase FastApi
app = FastAPI()

# Importamos la base de datos con los datos de los estudiantes
df = pd.read_excel("Data50.xlsx")

# Definimos el modelo de datos utilizando Pydantic
class Students(BaseModel): # Este modelo representa la estructura de los datos que vamos a manejar
    NombreCompleto: str
    Matricula: int
    Edad: int
    Carrera: str
    Sexo: str
    Correo: str
    Facultad: str
    AñoExamen: int
    Compañero: int
    Materia: str
    
# -------------------------------- API CRUD con FastAPI ----------------------------------
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< GET >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.get("/Estudiantes/") # Nivel 1
async def get_students(NombreCompleto: Optional[str] = None, Matricula: Optional[int] = None):
    if NombreCompleto:
        df_filtered = df[df['NombreCompleto'] == NombreCompleto]
    elif Matricula:
        df_filtered = df[df['Matricula'] == Matricula]
    else:
        df_filtered = df

    return df_filtered.to_dict(orient="records")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< POST >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.post("/Estudiantes/")
async def create_student(student: Students):
    if df[(df['Matricula'] == student.Matricula)].empty:
        new_student = student.dict() 
        df.loc[len(df)] = new_student
        df.to_excel("Data50.xlsx", index=False, engine='openpyxl') # Reemplazamos el archivo Excel con los nuevos datos
        
        ### Opcional: Guardar el nuevo estudiante en el archivo Excel
        # with pd.ExcelWriter("Data50.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        #     writer.book.active = 0
        #     sheet = writer.book.active
        #     inicio = sheet.max_row
        #     write_student = pd.DataFrame([new_student])
        #     write_student.to_excel(writer, index=False, header=False, startrow=inicio)
            
        return {"message": "Estudiante creado exitosamente", "student": new_student}
    else:
        return {"error": "El estudiante ya existe"}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PUT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.put("/Estudiantes/")
async def update_student(student: Students):
    if not df[(df['Matricula'] == student.Matricula)].empty: 
        row = df[df['Matricula'] == student.Matricula].index[0]          
        df.loc[row] = student.dict()  
        df.to_excel("Data50.xlsx", index=False, engine='openpyxl')
        
        return {"message": "Estudiante actualizado exitosamente", "student": student.dict()}
    
    return {"error": "Estudiante no encontrado"}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< DELETE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.delete("/Estudiantes/")
async def delete_student(student: Students):
    if not df[(df['Matricula'] == student.Matricula)].empty:
        df.drop(df[df['Matricula'] == student.Matricula].index, inplace=True)
        df.to_excel("Data50.xlsx", index=False, engine='openpyxl')
        
        return {"message": "Estudiante eliminado exitosamente"}
    
    return {"error": "Estudiante no encontrado"}
