One of the behavioural modification techniques requires a person to keep track of “the new thing” in order to enable the new behavioural pattern (by constant awareness). Things we track are things we tend to improve.
</br>Idea of this application is to improve the quality of meals we eat. It doesn’t provide any guidance, however it helps to see trends if we keep up with eating products we think we should:)

<b>How do I use it?</b>
- Run the application on a computer available from the local network.
  > python webserver.py  # note printed IP
- Open a web page using IP printed out by the app. (TIP: modify hosts file to simplify access, %SystemRoot%\System32\drivers\etc\hosts)
- Create a new profile and fill the “Ration” page with things you’d like to track.
- “Overview” page allows you to modify the current status of meals intake.

<b>Tech stuff</b>
- Flask for web, html templates and css (note: built-in development server is used for deployment)
- DB uses json for simplicity
