from django.views import View
from django.shortcuts import render
from .forms import FacebookPostForm
from .services.scraper import scrape_facebook_post
from .services.extractor import get_structured_content

class FacebookPostScraperView(View):
    form_template = "Scraper/scrape_post_form.html"
    result_template = "Scraper/scrape_post_details.html"
    def get(self, request):
        form = FacebookPostForm()
        return render(request,"Scraper/scrape_post_form.html", {"form": form})

    def post(self, request):
        form = FacebookPostForm(request.POST)
        context  = {"form": form}
        result = {}
        if form.is_valid():
            url = form.cleaned_data["url"]
            try:
                result = scrape_facebook_post(url)
                content_details = get_structured_content(result.get("content", ""))
                context.update({
                    "images": result.get("images", []),
                    "post": content_details
                })
            except Exception as e:
                context["error"] = f"Failed to scrape the post: {str(e)}"
            
        return render(request, self.result_template, context)
