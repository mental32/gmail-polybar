if [ -e ~/.config/polybar/gmail ]; then
	echo "Updating gmail-polybar..."
	cp polybar.py ~/.config/polybar/gmail/
else
	mkdir ~/.config/polybar/gmail
	cp polybar.py ~/.config/polybar/gmail/

	echo "[module/gmail]
	type = custom/script
	exec = python3 ~/.config/polybar/gmail/polybar.py
	tail = true
	click-left = xdg-open https://mail.google.com" >> ~/.config/polybar/config
fi

