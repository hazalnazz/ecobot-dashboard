import streamlit as st
import os
from pathlib import Path
import requests

def create_model_viewer_html(model_url, height):
    """
    Create HTML content for a 3D model viewer using Three.js.
    Assumes model_url is an absolute URL accessible by the browser.
    """
    unique_id = f"model-container-{height}-{hash(model_url) % 10000}"

    html = f"""
    <div style="height: {height}px; width: 100%; margin: 10px 0;">
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/loaders/GLTFLoader.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/controls/OrbitControls.js"></script>

        <div id="{unique_id}" style="width: 100%; height: 100%;">
            <div id="loading-indicator-{unique_id}" style="text-align: center; padding-top: 50px;">
                Loading 3D model...
            </div>
            <div id="error-container-{unique_id}" style="display:none; color:red; text-align:center; padding:20px;"></div>
        </div>

        <script>
            const container = document.getElementById('{unique_id}');
            const loadingIndicator = document.getElementById('loading-indicator-{unique_id}');
            const errorContainer = document.getElementById('error-container-{unique_id}');

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{antialias: true, alpha: true}});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setClearColor(0xf0f0f0, 1); // Light grey background
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 10, 7.5);
            scene.add(directionalLight);

            camera.position.set(5, 2, 5); // Adjusted camera position
            camera.lookAt(0, 0, 0);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = false;
            controls.minDistance = 2; // Prevent zooming too close
            controls.maxDistance = 15; // Prevent zooming too far
            controls.autoRotate = true;
            controls.autoRotateSpeed = 0.8;

            const loader = new THREE.GLTFLoader();
            let model;

            console.log('Attempting to load model from URL:', '{model_url}');

            loader.load('{model_url}',
                function(gltf) {{ // Success
                    loadingIndicator.style.display = 'none';
                    model = gltf.scene;

                    // Center and scale the model
                    const box = new THREE.Box3().setFromObject(model);
                    const center = box.getCenter(new THREE.Vector3());
                    model.position.sub(center); // Center the model

                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 4.0 / maxDim; // Scale to fit nicely
                    model.scale.set(scale, scale, scale);

                    scene.add(model);
                    console.log('Model successfully loaded:', '{model_url}');
                }},
                function(xhr) {{ // Progress
                    const percentComplete = xhr.loaded / xhr.total * 100;
                    loadingIndicator.textContent = `Loading: ${{Math.round(percentComplete)}}%`;
                    console.log(`Model loading progress: ${{Math.round(percentComplete)}}%`);
                }},
                function(error) {{ // Error
                    console.error('Error loading model:', error);
                    loadingIndicator.style.display = 'none';
                    errorContainer.style.display = 'block';
                    let errorDetails = JSON.stringify(error, Object.getOwnPropertyNames(error), 2);
                    if (errorDetails === '{{}}' && error.message) {{ // Handle cases where stringify is empty but message exists
                        errorDetails = error.message;
                    }} else if (errorDetails === '{{}}') {{
                        errorDetails = "Unknown error. Check browser console (F12) Network tab for details (e.g., 404 Not Found, CORS).";
                    }}

                    errorContainer.innerHTML = `
                        <strong>Error loading 3D model:</strong><br>
                        URL: <a href="{model_url}" target="_blank">{model_url}</a><br>
                        <pre style="text-align: left; color: #555; font-size: 80%; white-space: pre-wrap; word-wrap: break-word;">${{errorDetails}}</pre><br>
                        <div style="color: #444; font-size: 90%; text-align: left;">
                            <strong>Troubleshooting:</strong><br>
                            1. <strong>Is the static server running?</strong> Ensure <code>streamlit_static_server.py</code> is active in a separate terminal.<br>
                            2. <strong>Is the URL correct?</strong> Click the URL above. Does it show the file content or a 'Not Found' error?<br>
                            3. <strong>Check Browser Console:</strong> Press F12, go to the 'Console' and 'Network' tabs for more specific errors (like 404, CORS).<br>
                            4. <strong>Verify File Path:</strong> Confirm the model file exists at the path specified in <code>config.py</code>.<br>
                            5. <strong>Check Server Port:</strong> Ensure the port in <code>config.py</code> (STATIC_SERVER_URL) matches the port used by <code>streamlit_static_server.py</code> (currently 8502).
                        </div>
                    `;
                }}
            );

            function animate() {{
                requestAnimationFrame(animate);
                controls.update(); // Required for damping and auto-rotate
                renderer.render(scene, camera);
            }}

            animate();

            window.addEventListener('resize', function() {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </div>
    """
    return html

def get_model_url(model_path):
    """Returns the model URL, handling both local and remote paths."""
    return model_path  # All paths should now be URLs

def display_3d_model(model_url, height=400):
    """
    Display a 3D model in Streamlit using its URL.
    
    Args:
        model_url: URL to the GLTF model file
        height: Height of the viewer in pixels.
    """
    # Verify URL is accessible
    try:
        response = requests.head(model_url)
        if response.status_code != 200:
            raise Exception(f"URL returned status code {response.status_code}")
    except Exception as e:
        st.error(f"Error accessing model URL: {e}")
        st.markdown(f"""
        <div style="height: {height}px; border: 1px dashed red; display: flex; align-items: center; justify-content: center; flex-direction: column; padding: 10px;">
            <p style="color: red; font-weight: bold;">3D Model Error</p>
            <p style="font-size: small;">Could not access model URL:</p>
            <p style="font-size: small; font-family: monospace;">{model_url}</p>
            <p style="font-size: small;">Check your internet connection and model URL.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Generate and display the HTML component
    html_content = create_model_viewer_html(model_url, height)
    st.components.v1.html(html_content, height=height + 20)
