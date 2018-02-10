using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//using UnityEngine.Networking;
//using System.Text;
using Lib;
using System.Xml;
using System.IO;
using System.Text;
using System;

//public delegate void Logggggg(string response);

public class test : MonoBehaviour {
	void Start () {
//		//Test WebGet 
//		Dictionary<string,string> dic1 = new Dictionary<string, string> ();
//		dic1 ["token"] = "0U+kDyJ4d2PEPXxNfBrqVpKhdT+pjwUkGg0lqETNH9kMdXZKLLtjoy/aFEYjFawC";
//		NetworkManager.Singleton.WebGet ("https://qa.knowbox.cn:8004/poetry/poetry/get-poetry-page", dic1, (respons) => {
//			Debug.Log ("response : " + respons);
//		});
//		//Test WebPost 
//		Dictionary<string,string> dic = new Dictionary<string, string> ();
//		dic.Add("token","0U+kDyJ4d2PEPXxNfBrqVpKhdT+pjwUkGg0lqETNH9kMdXZKLLtjoy/aFEYjFawC");
//		dic.Add("courseSectionId", "417715");
//		dic.Add("levelId", "417718");
//		dic.Add("source", "iPhoneRCStudent");
//		dic.Add("version", "3.2.4");
//		dic.Add("answerList", "[{\"questionId\":\"2057873\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"A\\\"}]\"},{\"questionId\":\"2057874\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"C\\\"}]\"},{\"questionId\":\"2057875\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"C\\\"}]\"},{\"questionId\":\"2057876\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"A\\\"}]\"},{\"questionId\":\"2057877\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"A\\\"}]\"},{\"questionId\":\"2057878\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"C\\\"}]\"},{\"questionId\":\"2057879\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"A\\\"}]\"},{\"questionId\":\"2057887\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"B\\\"}]\"},{\"questionId\":\"2057888\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"A\\\"}]\"},{\"questionId\":\"2057889\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"B\\\"}]\"},{\"questionId\":\"2057890\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"A\\\"}]\"},{\"questionId\":\"2057891\",\"spendTime\":0,\"score\":\"0\",\"answer\":\"[{\\\"blank_id\\\":1,\\\"choice\\\":\\\"C\\\"}]\"}]");
//		NetworkManager.Singleton.WebPost ("https://qa.knowbox.cn:8004/poetry/poetry/submit-answer", dic, (string response) => {
//			Debug.Log ("post response : " + response);
//		});
		xml();
	}

	private void xml(){
		int count;
		byte[] byteArray;
		char[] charArray;
		UnicodeEncoding uniEncoding = new UnicodeEncoding();
		byte[] firstString = uniEncoding.GetBytes("努力学习");
		byte[] secondString = uniEncoding.GetBytes("不做C#中的菜鸟");
		using (MemoryStream memStream = new MemoryStream(100))
		{
			memStream.Write(firstString, 0, firstString.Length);
			count = 0;
			while (count < secondString.Length)
			{
				memStream.WriteByte(secondString[count++]);
			}
			string content = string.Format ("Capacity={0},Length={1},Position={2}\n", memStream.Capacity.ToString (), memStream.Length.ToString (), memStream.Position.ToString ());
			Debug.Log(content);
			memStream.Seek(0, SeekOrigin.Begin);
			byteArray = new byte[memStream.Length];
			count = memStream.Read(byteArray, 0, 20);
			while (count < memStream.Length)
			{
				byteArray[count++] = Convert.ToByte(memStream.ReadByte());
			}
			charArray = new char[uniEncoding.GetCharCount(byteArray, 0, count)];
			uniEncoding.GetDecoder().GetChars(byteArray, 0, count, charArray, 0);
			Debug.Log(charArray.ToString());
//			Console.ReadKey();
		}
	}
}
