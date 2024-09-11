from django.shortcuts import render
from .forms import SearchForm
import google.cloud.dlp
import os
import logging

logger = logging.getLogger(__name__)

def search(request):
    logger.debug("Inside Search")
    form = SearchForm()
    results = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Here you can handle the query and search your data models.
            # results = YourModel.objects.filter(name__icontains=query)
            #ogger.debug(f'Inside Search')
            print(f'Inside Search')
            results = dlp(query) 
            results = f'Search results for "{results}"'
    
    return render(request, 'AISP/home.html', {'form': form, 'results': results})



def dlp(request):
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ai-scam-spotter-micro-v1.json"
        dlp_client = google.cloud.dlp_v2.DlpServiceClient()
        print(f'Inside dlp')
        # The string to inspect
        content = request
        # Construct the item to inspect.
        item = {"value": content}

        # The info types to search for in the content. Required.
        info_types = [{"name": "EMAIL_ADDRESS"}, {"name": "FIRST_NAME"},  {"name": "LAST_NAME"},{"name": "CREDIT_CARD_NUMBER"}]

        # The minimum likelihood to constitute a match. Optional.
        min_likelihood = google.cloud.dlp_v2.Likelihood.LIKELIHOOD_UNSPECIFIED

        # The maximum number of findings to report (0 = server maximum). Optional.
        max_findings = 0

        # Whether to include the matching string in the results. Optional.
        include_quote = True

        # Construct the configuration dictionary. Keys which are None may
        # optionally be omitted entirely.
        inspect_config = {
            "info_types": info_types,
            "min_likelihood": min_likelihood,
            "include_quote": include_quote,
            "limits": {"max_findings_per_request": max_findings},
        }
        print(f'Inside dlp')
        # Convert the project id into a full resource id.
        project_id = "ai-scam-spotter-micro-v1"
        parent = f"projects/{project_id}"

        # Call the API.
        response = dlp_client.inspect_content(
            request={"parent": parent, "inspect_config": inspect_config, "item": item}
        )
        print(f'Inside dlp')
        out ="Likelihood : "
        out2  ="Quote"
        # Print out the results.
        if response.result.findings:
            print(f'Inside dlp')
            for finding in response.result.findings:
                try:
                    print(f"Quote: {finding.quote}")
                except AttributeError:
                    pass
                print(f"Info type: {finding.info_type.name}")
                # Convert likelihood value to string respresentation.
                likelihood = finding.likelihood.name
                print(f"Likelihood: {likelihood}")
                print(f"---------------")
                out = out + likelihood
                out2= out2+ finding.quote
            print(f'OUT')
        else:
            print(f"No findings.")

        return out + out2
    
    except Exception as e:
        print(f'{e}')