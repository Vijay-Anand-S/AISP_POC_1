import google.cloud.dlp
import os
# Instantiate a client.

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ai-scam-spotter-micro-v1.json"
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
dlp_client = google.cloud.dlp_v2.DlpServiceClient()



# The string to inspect
content = "I am Robert and my email is robertB@gmail.com. Here is my CC number 378282246310005"

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

# Convert the project id into a full resource id.
project_id = "ai-scam-spotter-micro-v1"
parent = f"projects/{project_id}"

# Call the API.
response = dlp_client.inspect_content(
    request={"parent": parent, "inspect_config": inspect_config, "item": item}
)

# Print out the results.
if response.result.findings:
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
else:
    print("No findings.")