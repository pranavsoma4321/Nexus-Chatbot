import os
import numpy as np
import cv2
import base64
import io
import json
import warnings
warnings.filterwarnings('ignore')

# Try to import optional libraries
try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available - using fallback functionality")

try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ImportError:
    OPEN3D_AVAILABLE = False
    print("Open3D not available - 3D features disabled")

try:
    import torch
    from diffusers import StableDiffusionPipeline
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch/Diffusers not available - using fallback image generation")

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import trimesh
    TRIMESH_AVAILABLE = True
except ImportError:
    TRIMESH_AVAILABLE = False

class AIImageProcessor:
    def __init__(self):
        self.device = "cuda" if (TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
        print(f"Using device: {self.device}")
        print(f"PIL Available: {PIL_AVAILABLE}")
        print(f"Open3D Available: {OPEN3D_AVAILABLE}")
        print(f"Torch Available: {TORCH_AVAILABLE}")
        
        # Initialize text-to-image model (will download on first use)
        try:
            self.text2img_pipe = None  # Lazy loading
            print("Text-to-Image model ready for lazy loading")
        except Exception as e:
            print(f"Text-to-Image model initialization failed: {e}")
            self.text2img_pipe = None
    
    def load_text2img_model(self):
        """Lazy load the text-to-image model"""
        if self.text2img_pipe is None:
            try:
                print("Loading Stable Diffusion model...")
                self.text2img_pipe = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                self.text2img_pipe = self.text2img_pipe.to(self.device)
                print("Model loaded successfully!")
            except Exception as e:
                print(f"Failed to load model: {e}")
                return None
        return self.text2img_pipe
    
    def text_to_image(self, prompt, negative_prompt="", width=512, height=512):
        """Generate image from text using Stable Diffusion"""
        try:
            pipe = self.load_text2img_model()
            if pipe is None:
                # Fallback: create a simple colored image with text
                return self.create_fallback_image(prompt)
            
            with torch.no_grad():
                result = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=20,
                    guidance_scale=7.5
                )
            
            # Convert PIL image to base64
            image = result.images[0]
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image': img_str,
                'prompt': prompt
            }
            
        except Exception as e:
            print(f"Text-to-image generation failed: {e}")
            return self.create_fallback_image(prompt)
    
    def create_fallback_image(self, prompt):
        """Create a fallback image when AI model is not available"""
        try:
            if not PIL_AVAILABLE:
                return {
                    'success': False,
                    'error': 'PIL library not installed. Install with: pip install Pillow'
                }
            
            # Create a simple gradient image with text
            img = Image.new('RGB', (512, 512), color=(50, 50, 100))
            
            # Add some visual elements based on prompt
            if "car" in prompt.lower():
                # Draw simple car shape
                draw = ImageDraw.Draw(img)
                draw.rectangle([150, 200, 350, 300], fill=(200, 50, 50))
                draw.ellipse([180, 280, 220, 320], fill=(50, 50, 50))
                draw.ellipse([280, 280, 320, 320], fill=(50, 50, 50))
            
            # Add text
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            text_lines = [prompt[i:i+30] for i in range(0, len(prompt), 30)]
            y_pos = 50
            for line in text_lines:
                draw.text((50, y_pos), line, fill=(255, 255, 255), font=font)
                y_pos += 30
            
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image': img_str,
                'prompt': prompt,
                'fallback': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to create fallback image: {e}"
            }
    
    def image_to_3d(self, image_data, depth_scale=1.0):
        """Convert 2D image to 3D mesh using depth estimation"""
        try:
            if not PIL_AVAILABLE:
                return {
                    'success': False,
                    'error': 'PIL library not installed. Install with: pip install Pillow'
                }
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale for depth estimation
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Simple depth estimation using gradient
            # Create depth map based on brightness and edges
            depth = cv2.Laplacian(gray, cv2.CV_64F)
            depth = cv2.GaussianBlur(depth, (5, 5), 0)
            
            # Normalize depth
            depth = (depth - depth.min()) / (depth.max() - depth.min())
            depth = depth * depth_scale
            
            # Use appropriate method based on available libraries
            if OPEN3D_AVAILABLE:
                print("Using Open3D for 3D generation...")
                return self.create_obj_file_with_open3d(img_array, depth)
            else:
                print("Open3D not available, using simple OBJ generation...")
                return self.create_simple_obj_file(img_array, depth)
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to convert image to 3D: {e}"
            }
    
    def create_simple_obj_file(self, img_array, depth):
        """Create simple OBJ file without Open3D"""
        try:
            h, w = depth.shape
            x, y = np.meshgrid(np.arange(w), np.arange(h))
            z = depth
            
            # Create vertices
            vertices = np.stack([x.flatten(), y.flatten(), z.flatten()], axis=1)
            
            # Create faces (triangles)
            faces = []
            for i in range(h - 1):
                for j in range(w - 1):
                    v1 = i * w + j
                    v2 = i * w + (j + 1)
                    v3 = (i + 1) * w + j
                    v4 = (i + 1) * w + (j + 1)
                    
                    faces.append([v1, v2, v3])
                    faces.append([v2, v4, v3])
            
            # Create OBJ file content with proper format
            obj_content = []
            
            # Add header comment
            obj_content.append("# Generated by Nexus AI Image Processor")
            obj_content.append(f"# Vertices: {len(vertices)}, Faces: {len(faces)}")
            obj_content.append("")
            
            # Add vertices (OBJ format: v x y z)
            for vertex in vertices:
                obj_content.append(f"v {vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}")
            
            obj_content.append("")
            
            # Add vertex colors as material (if available)
            if len(img_array.shape) == 3:
                obj_content.append("# Vertex colors (RGB)")
                colors = img_array.reshape(-1, 3)
                for i, color in enumerate(colors):
                    # Normalize colors to 0-1 range for OBJ
                    r, g, b = color[0]/255.0, color[1]/255.0, color[2]/255.0
                    obj_content.append(f"vc {r:.6f} {g:.6f} {b:.6f}")
            
            obj_content.append("")
            
            # Add faces (OBJ format uses 1-based indexing)
            obj_content.append("# Faces")
            for face in faces:
                # OBJ format: f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3
                # We'll use simple format: f v1 v2 v3
                obj_content.append(f"f {face[0]+1} {face[1]+1} {face[2]+1}")
            
            obj_data = "\n".join(obj_content)
            model_base64 = base64.b64encode(obj_data.encode('utf-8')).decode()
            
            return {
                'success': True,
                'model': model_base64,
                'format': 'obj',
                'vertices': len(vertices),
                'faces': len(faces),
                'method': 'simple'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Simple OBJ creation failed: {e}"
            }
    
    def text_to_3d(self, text_prompt):
        """Generate 3D model from text description"""
        try:
            # First generate image from text
            image_result = self.text_to_image(text_prompt)
            if not image_result['success']:
                return image_result
            
            # Then convert image to 3D
            image_data = f"data:image/png;base64,{image_result['image']}"
            model_result = self.image_to_3d(image_data, depth_scale=2.0)
            
            if model_result['success']:
                model_result['prompt'] = text_prompt
                model_result['generated_from'] = 'text'
            
            return model_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to generate 3D from text: {e}"
            }
    
    def apply_image_filter(self, image_data, filter_type):
        """Apply various filters to image"""
        try:
            if not PIL_AVAILABLE:
                return {
                    'success': False,
                    'error': 'PIL library not installed. Install with: pip install Pillow'
                }
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            print(f"Original image mode: {image.mode}, size: {image.size}")
            
            # Convert to RGB to handle palette images
            if image.mode != 'RGB':
                image = image.convert('RGB')
                print(f"Converted to RGB, new mode: {image.mode}")
            
            # Apply filter
            if filter_type == 'grayscale':
                processed = image.convert('L')
                # Convert back to RGB for consistency
                processed = processed.convert('RGB')
                print("Applied grayscale filter")
            elif filter_type == 'blur':
                processed = image.filter(ImageFilter.GaussianBlur(radius=5))
                print("Applied blur filter")
            elif filter_type == 'sharpen':
                processed = image.filter(ImageFilter.SHARPEN)
                print("Applied sharpen filter")
            elif filter_type == 'brightness':
                enhancer = ImageEnhance.Brightness(image)
                processed = enhancer.enhance(1.5)
                print("Applied brightness filter")
            elif filter_type == 'contrast':
                enhancer = ImageEnhance.Contrast(image)
                processed = enhancer.enhance(1.5)
                print("Applied contrast filter")
            elif filter_type == 'sepia':
                processed = image.convert('RGB')
                pixels = np.array(processed)
                # Sepia transformation
                sepia_filter = np.array([
                    [0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]
                ])
                sepia_img = pixels.dot(sepia_filter.T)
                sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
                processed = Image.fromarray(sepia_img)
                print("Applied sepia filter")
            elif filter_type == 'invert':
                processed = Image.fromarray(255 - np.array(image))
                print("Applied invert filter")
            elif filter_type == 'edge':
                # Edge detection
                gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                # Convert back to RGB for consistency
                processed = Image.fromarray(edges, mode='L').convert('RGB')
                print("Applied edge detection filter")
            elif filter_type == 'emboss':
                processed = image.filter(ImageFilter.EMBOSS)
                print("Applied emboss filter")
            else:
                processed = image
                print(f"Unknown filter: {filter_type}, using original image")
            
            # Convert back to base64
            buffered = io.BytesIO()
            processed.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            print(f"Successfully processed {filter_type} filter")
            
            return {
                'success': True,
                'image': img_str,
                'filter': filter_type
            }
            
        except Exception as e:
            print(f"Error in apply_image_filter: {e}")
            print(f"Filter type: {filter_type}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f"Failed to apply filter: {e}"
            }
    
    def detect_faces(self, image_data):
        """Detect faces in image"""
        try:
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Decode image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(image)
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img_array, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Convert back to image
            processed = Image.fromarray(img_array)
            
            # Convert to base64
            buffered = io.BytesIO()
            processed.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image': img_str,
                'faces_found': len(faces),
                'coordinates': faces.tolist()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Face detection failed: {e}"
            }

# Initialize the processor
processor = AIImageProcessor()

if __name__ == "__main__":
    # Test the processor
    print("Testing AI Image Processor...")
    
    # Test text to image
    result = processor.text_to_image("red sports car")
    print(f"Text-to-image result: {result['success']}")
    
    # Test image to 3D (if we have an image)
    # result = processor.image_to_3d("data:image/png;base64,...")
    # print(f"Image-to-3D result: {result['success']}")
    
    print("AI Image Processor ready!")
