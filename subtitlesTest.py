import requests

json = {
 'source': {
  'output_format': 'mp4',
  'elements': [
   {
    'type': 'video',
    'id': '17ca2169-786f-477f-aaea-4a2598bf24eb',
    'source': 'https://cdn.creatomate.com/demo/the-daily-stoic-podcast.mp4'
   },
   {
    'type': 'text',
    'transcript_source': '17ca2169-786f-477f-aaea-4a2598bf24eb',
    'transcript_effect': 'highlight',
    'transcript_maximum_length': 14,
    'y': '82%',
    'width': '81%',
    'height': '35%',
    'x_alignment': '50%',
    'y_alignment': '50%',
    'fill_color': '#ffffff',
    'stroke_color': '#000000',
    'stroke_width': '1.6 vmin',
    'font_family': 'Montserrat',
    'font_weight': '700',
    'font_size': '9.29 vmin',
    'background_color': 'rgba(216,216,216,0)',
    'background_x_padding': '31%',
    'background_y_padding': '17%',
    'background_border_radius': '31%'
   }
  ]
 }
}

response = requests.post(
 'https://api.creatomate.com/v1/renders',
 headers={
  # Find your API key under 'Project Settings' in your account:
  # https://creatomate.com/docs/api/rest-api/authentication
  'Authorization': 'Bearer Your-API-Key',
  'Content-Type': 'application/json',
 },
 json=json,
)

# Wait a minute, then visit the URL provided in the response:
print(response.json())

