
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings-debug')
django.setup()

from dsa.models import Comment, Feedback

def main():
    count = 100
    with open("comments_cleaned.txt", "r", encoding="utf-8") as f:
        for line in f:
            if count <= 0:
                break
                
            comment_text = line.strip()
            if comment_text:
                comment = Comment.objects.create(text=comment_text)
                count -= 1

if __name__ == "__main__":
    main()