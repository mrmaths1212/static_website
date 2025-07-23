from textnode import TextNode, TextType
from extractmarkdown import *
from blocks_to_html import *

import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Lire le fichier markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convertir le markdown en HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extraire le titre
    title = extract_title(markdown_content)

    # Lire le fichier template
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Remplacer les variables dans le template
    filled_template = (
        template_content
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
    )

    # Créer le dossier de destination si nécessaire
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Écrire le fichier HTML final
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(filled_template)

    print(f"✅ Page written to {dest_path}")

def copy_static(source_dir, dest_dir):
    # Supprimer le dossier de destination s'il existe déjà
    if os.path.exists(dest_dir):
        print(f"Deleting existing destination: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Recréer le dossier de destination vide
    os.makedirs(dest_dir)

    # Copie récursive
    def copy_recursive(src, dst):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isdir(src_path):
                print(f"Creating directory: {dst_path}")
                os.makedirs(dst_path, exist_ok=True)
                copy_recursive(src_path, dst_path)
            else:
                print(f"Copying file: {src_path} -> {dst_path}")
                shutil.copy2(src_path, dst_path)

    # Lancer la copie
    copy_recursive(source_dir, dest_dir)

def generate_page_recursively(source_dir, template_path, dest_dir):
    # Parcourir tous les fichiers dans le dossier source
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                # Construire les chemins complets
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, source_dir)
                dest_path = os.path.join(dest_dir, relative_path.replace(".md", ".html"))

                # Créer les dossiers nécessaires dans le dossier de destination
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Générer la page
                generate_page(from_path, template_path, dest_path)

def main():
    # 1. Supprimer le contenu du dossier `public` s'il existe
    if os.path.exists("public"):
        shutil.rmtree("public")
        print("✅ Deleted existing 'public' directory.")

    # 2. Copier tous les fichiers statiques dans `public`
    copy_static("static", "public")

    generate_page_recursively("content", "template.html", "public")

# Lancer la fonction si exécuté en script
if __name__ == "__main__":
    main()

