from textnode import TextNode, TextType
from extractmarkdown import *
from blocks_to_html import *

import os
import shutil
import sys

def generate_page(from_path, template_path, dest_path, base_path):
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

    filled_template = filled_template.replace('href="/', f'href="{basepath}')
    filled_template = filled_template.replace('src="/', f'src="{basepath}')
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith(".md"):
                # Chemin absolu vers le fichier .md
                from_path = os.path.join(root, filename)

                # Calcul du chemin relatif à dir_path_content
                relative_path = os.path.relpath(from_path, dir_path_content)

                # Destination : même structure dans dest_dir_path, avec .html à la place de .md
                dest_path = os.path.join(
                    dest_dir_path,
                    os.path.splitext(relative_path)[0] + ".html"
                )

                # Créer les dossiers de destination si besoin
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Générer la page
                print(f"📄 Generating page from {from_path} to {dest_path}")
                generate_page(from_path, template_path, dest_path, base_path)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # 1. Supprimer le contenu du dossier `public` s'il existe
    if os.path.exists("public"):
        shutil.rmtree("public")
        print("✅ Deleted existing 'public' directory.")

    # 2. Copier tous les fichiers statiques dans `public`
    copy_static("static", "public")

    generate_pages_recursive("content", "template.html", "public", basepath)

# Lancer la fonction si exécuté en script
if __name__ == "__main__":
    main()

