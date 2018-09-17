mkdir ~/.config/polybar/gmail

cp polybar.py ~/.config/polybar/gmail

echo "[module/gmail]
type = custom/script
exec = ~/.config/polybar/gmail/polybar.py
tail = true
click-left = xdg-open https://mail.google.com" >> ~/.config/polybar/config
