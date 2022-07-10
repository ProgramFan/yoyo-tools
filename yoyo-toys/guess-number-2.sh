#!/bin/bash
#

bomb="💣"
firecracker="🧨"
horry="🎉"
messages=("$bomb" "$firecracker" "$horry" "$bomb" "$bomb")

number=$((RANDOM % 10 + 1))
angry_id=0

function angry() {
	angry_id=$((angry_id + 1))
	if [[ $angry_id -eq 1 ]]; then
		echo -n $firecracker
		echo "不要再乱输入了，我有点生气了！"
	elif [[ $angry_id -eq 2 ]]; then
		echo -n $bomb
		echo "你再乱输入我就发狂了！！"
	elif [[ $angry_id -eq 3 ]]; then
		echo -n $bomb$bomb$bomb
		echo "你再乱输入我就炸死你！！！"
	else
		while true; do
			echo -n ${messages[$(($RANDOM % 5))]}
		done
	fi
}

function guess_number() {
	echo -n "猜一猜我的数字是什么："
	read -r inp
	if [[ $inp =~ ^[0-9]{1,5}$ ]]; then
		if [ "$inp" -eq $number ]; then
			echo "恭喜你猜对了 $horry$horry$horry"
			exit 0
		elif [ "$inp" -gt $number ]; then
			echo "很遗憾猜大了，继续努力。"
		elif [ "$inp" -lt $number ]; then
			echo "很遗憾猜小了，继续努力。"
		fi
	else
		angry
	fi
}

while true; do
	guess_number
done
