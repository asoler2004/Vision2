import os
import base64
from flask import Flask, request,jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Any

load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SECRET_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Por favor configura las credenciales de Supabase")

def create_supabase_client(url: str, key: str) -> Client:
    """Create Supabase client"""
    try:
        return create_client(url, key)
        print(f"Supabase conectado")
    except Exception as e:
        print(f"Error conectando a Supabase: {str(e)}")
        return None

supabase = create_supabase_client(supabase_url, supabase_key)

def upload_image_to_supabase(supabase: Client, file_content: bytes, user_id: str, story_title: str, timestamp: str) -> str:
    """Upload image to Supabase storage and return the public URL"""
    try:
        # Download image
        if not file_content:
            return None
        file_extension =  'jpg'
               
        # Generate unique, sanitized filename
        filename = f"{user_id}_{timestamp}.{file_extension}"
        # print(filename)
        # Upload to storage
        # 
        # result = supabase.storage.from_("story-images").upload(filename, image_data)

        response = supabase.storage.from_("story-images").upload(filename, file_content)
        # print("supabase response: ",response)
        public_url = supabase.storage.from_("story-images").get_public_url(filename)
        # print("public_url", public_url)
        return public_url
        # return jsonify({
        #     'success': True,
        #     'message': "Imagen subida exitosamente",
        #     'filename': filename,
        #     'url': public_url}), 200
            
    except Exception as e:
        return jsonify({'error': f"Error procesando imagen: {str(e)}"}),500

@app.route('/')
def index():
    return "Hola! Este es el servidor de historias en Supabase"


@app.route('/upload', methods=['POST'])
def upload_to_supabase():
    """Upload story to Supabase database with images uploaded to storage
       Expected JSON:
       {'user_id': str(user_id),
        'title': 'title',
        'content': content,
        'tone': str(tone),
        'images': uploaded_image_urls,  # Store Supabase URLs in images array
        'status': 'published',
        'metadata': {
                'platform': 'facebook', 
                'license': 'license',
                'album_id': 'album_id',
                'original_story_id': story_ids[0] if len(story_ids) > 0 else None,
                'original_image_urls': original_image_urls  # Keep reference to original URLs
            }
        'version': 1,
        'imagedata':"base64_encoded_data",
               
        }
    """
    try:
        story_data = request.json
        # print(story_data.keys())
        if not story_data:
            return jsonify({'error': 'No hay datos'}), 400
        
        
        user_id = story_data['user_id']
        title = str(story_data['title'])
        content = story_data['content']
        tone = str(story_data['tone'])
        images = story_data.get['images', []]  # Store Supabase URLs in images array
        status = story_data.get['status', 'published']
        metadata = story_data.get['metadata', {}]
        version = story_data.get['version', 1] 
        image_data = story_data.get['imagedata', '']
        # mimetype = story_data.get('mimetype','application/octet-stream')

        # print('user_id = ', user_id)
        # print('title = ', title)
        # # print('content = ',content)
        # print('tone = ',tone)
        # print('images = ',images)  # Store Supabase URLs in images array
        # print('status = ',status)
        # print('metadata = ',metadata)
        # print('version = ', version) 
        # # print('image_data = ', image_data)
        # Decode base64 data
        try:
            file_content = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'error': f'Invalid base64 data: {str(e)}'}),400

        # Get original image URLs - convert arrays to lists
        # original_image_urls = to_list(story_data['image_url'])
        # story_ids = to_list(story_data['story_id'])
        
        # Upload images to Supabase storage
        # print("📤 Subiendo imágenes al almacenamiento de Supabase...")
        # print('file content length:',len(file_content))
        uploaded_image_urls = []
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # print('timestamp: ',timestamp)
        
        uploaded_url = upload_image_to_supabase(supabase, file_content, user_id, title, timestamp)
        
        # print("json_result.content: ",json_result.content)
        total_images = 1   #len(original_image_urls)
        
        # for i, img_url in enumerate(original_image_urls):
        #     progress_bar.progress((i + 1) / total_images)
        #     print(f"Subiendo imagen {i + 1} de {total_images}...")
        
        if uploaded_url:
            uploaded_image_urls = [uploaded_url]
            print("imagen subida exitosamente.")
        else:
            print(f"No se pudo subir la imagen ")
        
        # print(uploaded_url, uploaded_image_urls)

        # print("story_data = ",story_data)
        print("uploaded_image_urls = ", uploaded_image_urls)
        # Format content with uploaded image URLs

        content = format_story_content(story_data, uploaded_image_urls)
        
        print("content: ", content)

        # Prepare data for insertion
        story_record = {
            'user_id': user_id,
            'title': story_data['title'],
            'content': content,
            'tone': tone,
            'images': uploaded_image_urls,  # Store Supabase URLs in images array
            'status': 'published',
            'metadata': {
                'license': story_data['license'],
                'album_id': story_data['album_id'],
                'original_story_id':  "",
                'original_image_urls': ""
            }
        }
        

        print("story record: ", story_record)

        result = supabase.table('stories').insert(story_record).execute()
        print(result)
        # Check result more safely
        if result :
            print(f"🎉 Historia '{story_data['title']}' subida exitosamente!")
            return jsonify({'success': True, 'message': 'Historia subida exitosamente'}), 200
        else:
            print("Error al subir la historia - no se recibieron datos")
            return jsonify({'success': False, 'error': 'no se recibieron datos'}), 400
            
    except Exception as e:
        error_msg = str(e)
        if "row-level security policy" in error_msg:
            print("❌ Error de política RLS: El usuario no tiene permisos para insertar datos")
            print("💡 Soluciones posibles:")
            print("1. Usa una clave de servicio en lugar de clave anónima")
            print("2. Modifica las políticas RLS en Supabase para permitir inserciones públicas")
            print("3. Implementa autenticación de usuario en la aplicación")
        else:
            print(f"Error subiendo a Supabase: {error_msg}")
            print(f"Detalles del error: {type(e).__name__}")
        return jsonify({'success': False, 'error': error_msg}), 500



        #     selected_tone = ""

        #     if supabase:
        #         use_service_key = True
        #         upload_to_supabase(supabase, story, user_id, selected_tone, use_service_key)
        # else:
    

# def parse_story_data(story_dict: Dict) -> Dict:
#     """Parse story dictionary to extract structured data"""
#     if isinstance(story_dict, str):
#         story_dict = ast.literal_eval(story_dict)
    
#     return {
#         'image_id': story_dict.get('image_id', []),
#         'image_url': story_dict.get('image_url', []),
#         'story_index': story_dict.get('story_index', []),
#         'story_id': story_dict.get('story_id', []),
#         'text': story_dict.get('text', [])
#     }

def is_array_like(obj) -> bool:
    """Check if object is array-like (list, numpy array, etc.)"""
    return hasattr(obj, '__iter__') and not isinstance(obj, (str, dict))



def download_image(url: str) -> bytes:
    """Download image from URL and return bytes"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error descargando imagen de {url}: {str(e)}")
        return None


def format_story_content(story_data: Dict, uploaded_image_urls: List[str] = None) -> Dict:
    """Format story data for Supabase upload"""
    
    texts = [story_data['text']]
    print ("texts: ", texts)
    # Create structured content - store all texts in body array as requested
    content = {
        "title": story_data['title'],
        "hook": texts[0] if len(texts) > 0 else "",
        "body": texts,  # Store all story texts in body array
        "call_to_action": texts[-1] if len(texts) > 1 else "",
        "full_text": texts[0]
    }
    print("content = ", content)
    return content

@app.route('/health',methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

# Main app
# def main():
#     # Parse and display story content
#     try:
#         story_data = parse_story_data(story['story'])
#         # Display story with images - convert arrays to lists
#         texts = to_list(story_data['text'])
#         images = to_list(story_data['image_url'])
#         if supabase_url and supabase_key:
#             selected_tone = ""
#             supabase = create_supabase_client(supabase_url, supabase_key)
#             if supabase:
#                 use_service_key = True
#                 upload_to_supabase(supabase, story, user_id, selected_tone, use_service_key)
#             else:
#                 print("Por favor configura las credenciales de Supabase")
                
#         except Exception as e:
#             print(f"Error procesando datos de la historia: {str(e)}")

#     else:
#         if df is not None:
#             print("👆 Crea una historia ")

if __name__ == "__main__":
    app.run(debug=True, host= 'localhost', port= 5000)
