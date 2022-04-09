mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"email@domain\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
maxUploadSize=10\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
