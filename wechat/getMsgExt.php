<?
	$str = $_POST['str'];
	$url = $_POST['url'];//先获取到两个POST变量
	//先针对url参数进行操作
	parse_str(parse_url(htmlspecialchars_decode(urldecode($url)),PHP_URL_QUERY ),$query);//解析url地址
	$biz = $query['__biz'];//得到公众号的biz
	$sn = $query['sn'];
	//再解析str变量
	$json = json_decode($str,true);//进行json_decode

	//$sql = "select * from `文章表` where `biz`='".$biz."' and `content_url` like '%".$sn."%'" limit 0,1;
	//根据biz和sn找到对应的文章

	$read_num = $json['appmsgstat']['read_num'];//阅读量
	$like_num = $json['appmsgstat']['like_num'];//点赞量
	//在这里同样根据sn在采集队列表中删除对应的文章，代表这篇文章可以移出采集队列了
	//$sql = "delete from `队列表` where `content_url` like '%".$sn."%'" 
	            
	//然后将阅读量和点赞量更新到文章表中。
	exit(json_encode($msg));//可以显示在anyproxy的终端里
?>