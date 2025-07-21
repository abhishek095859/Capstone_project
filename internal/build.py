import os
import subprocess

def write_dockerfile(stack, app_path):
    stack = stack.lower().strip()
    dockerfile_path = os.path.join(app_path, "Dockerfile")


    if stack == "vite":
        content = """
        FROM node:22
        WORKDIR /app
        COPY . .
        RUN npm install && npm run build
        RUN npm install -g serve
        CMD ["serve", "-s", "dist", "-l", "80"]
        """
    elif stack == "react":
        content = """
        FROM node:18
        WORKDIR /app
        COPY . .
        RUN npm install && npm run build
        RUN npm install -g serve
        CMD ["serve", "-s", "build", "-l", "80"]
        """
    elif stack == "html":
        content = """
        FROM nginx:alpine
        COPY . /usr/share/nginx/html
        EXPOSE 80
        CMD ["nginx", "-g", "daemon off;"]
        """
    else:
        raise Exception(f"....... Unknown stack: '{stack}' (expected 'vite', 'react', or 'html')")

    with open(dockerfile_path, "w") as f:
        f.write(content.strip())

    print(f"<><> Dockerfile written to {dockerfile_path}")

