from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re

class TextProcessor:

  def __init__(self, client):
    self.client = client

  def generate_transcript_from_idea(self, client, idea):
    response = client.chat.completions.create(
      # could use 3.5 turbo or gpt 4, but gpt 3.5 turbo is the most cost effective
      model="gpt-4o-mini-2024-07-18",
      messages=[
        {"role": "system", "content": "You are a writer for TikTok, Youtube Shorts, and Instagram Reels. You are to take a provided idea and generate a short video script about that idea. The video should be around 60 seconds long, so no more than 300 words. The video should be presented in \"video essay\" form and appeal to the emotions of the audience. The audience primed towards emotionally raw and dramatic content, but is very keen on the truth, so nothing should be false. Exaggerate the importance of something if it makes it cooler, but do not make anything up. The goal is to keep the younger generation informed while competing with the other content on these platforms. Everything should be presented in an authoritative, matter of fact tone. DO NOT direct the video. Only include the content that the narrator will read. This is a direct retelling of events, not a documentary. DO NOT include any music or sound effects. DO NOT include any video or images, or cinematography techniques. Only include the CONTENT of the video. DO NOT include items such as cut to, fade in, opening shot, closing shot, etc. DO NOT number the lines, or put ANYTHING other than the plain text of the script. Start the script with a strong opening, such as a startling fact or statistic (Did you know that every second, a slice of rainforest the size of a football field is lost?), a provocative question (Have you ever wondered what the world would look like if bees went extinct?), or a teaser (In just a moment, you'll discover the unexpected truth behind the world's most mysterious ancient structures). Structure the script with a narrative structure, with a clear beginning middle and end. Aim to evoke emotions - humor, surprise, empathy. Emotional content is more likely to be remembered and shared. While it is emotional, always make sure that it has substance. Make sure the viewer walks away with something to remember and tell their friends."},
        {"role": "user", "content": "Create the transcript about: " +  idea}
      ]
    )
    transcript_array = self.transcript_to_array(response)
    return transcript_array

  def transcript_to_array(self, transcript):
    transcript_text = transcript.choices[0].message.content
    cleaned_transcript = re.sub(r'Narrator: ?\"?', '', transcript_text)
    cleaned_transcript = re.sub(r'\"', '', cleaned_transcript)

    terminal_punctuation_marks = r'[.!?](?=\s|$)'
    sentences = re.split(terminal_punctuation_marks, cleaned_transcript)
    split_transcript = [sentence.strip() for sentence in sentences if sentence.strip()]

    cleaned_split_transcript = []

    for segment in split_transcript:
      segment = re.sub(r'\[.*?\]', '', segment) # remove any text in brackets
      segment = segment.replace('\n', ' ') # remove any new lines
      segment = re.sub(r'\s+', ' ', segment) # remove any extra spaces

      if len(segment.strip()) < 5:
        continue

      segment = segment.strip() + ". "

      cleaned_split_transcript.append(segment)

    return cleaned_split_transcript

  def generate_ideas_from_subject(self, client, subject):
    response = client.chat.completions.create(
      model="ft:gpt-3.5-turbo-1106:franklin-high-school::8ZBk0aP5",
      # this is a fine tuned model to create specific structured outputs
      messages=[
        {"role": "system", "content": "You are to generate many ideas about a provided subject. The goal of these ideas is to eventually create short videos about these topic, so they should about interesting and engaging topics. Each idea should explore only one miniature subtopic of the subject. Prioritize \"cool\" ideas and make sure only include ideas if they have the opportunity to appeal to the pathos. Each topic should be of a super specific topic or point in time and not a general idea. For example, \"The history of pirates\" is too broad, but \"Blackbeard Terrorizes Charleston, 1718\" is specific enough."},
        {"role": "user", "content": "Generate the ideas about: " +  subject}
      ]
    )

    response = response.choices[0].message.content
    ideas = response.split("\n")
    
    return ideas
