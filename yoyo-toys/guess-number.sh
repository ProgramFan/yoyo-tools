#!/bin/bash
#

bomb="💣"
firecracker="🧨"
horry="🎉"
messages=($bomb $firecracker $horry $bomb $bomb)

number=$(($RANDOM % 10 + 1))
angry_id=0

function angry() {
	angry_id=$(($angry_id + 1))
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
		while [[ 1 ]]; do
			echo -n ${messages[$(($RANDOM % 5))]}
		done
	fi
}

function guess_number() {
	echo -n "猜一猜我的数字是什么："
	read inp
	if [[ $inp =~ ^[0-9]{1,5}$ ]]; then
		if [ "$inp" -eq $number ]; then
			echo "恭喜你猜对了 $horry$horry$horry"
			exit 0
		else
			echo "很遗憾猜错了，继续努力。"
		fi
	else
		angry
	fi
}

while [[ 1 ]]; do
	guess_number
done
