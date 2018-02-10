using System;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

namespace Lib{
	public class NetworkManager : TSingleton<NetworkManager> {
		private MonoBehaviour _CoroutineBehaviour;
		public MonoBehaviour CoroutineBehaviour{
			get{ 
				if (_CoroutineBehaviour == null) {
					GameObject obj = GameObject.Find ("Main");
					if (obj != null)
						_CoroutineBehaviour = obj.GetComponent<ClientApp> ();
				}
				return _CoroutineBehaviour;
			}
		}
		private NetworkManager(){
		}

		//Web Get
		public void WebGet(string url, Dictionary<string,string> info,CallBack_None_Params_String handler){
				CoroutineBehaviour.StartCoroutine (_webGet (url, info, handler));
		}
		private string AppendUrl(string url,Dictionary<string,string> info){
			if (info == null)
				return url;

			StringBuilder builder = new StringBuilder (url);
			builder.Append("?");
			int count = 0;
			foreach (KeyValuePair<string,string> kv in info) {
				count++;
				if (count < info.Count - 1) {
					builder.Append (kv.Key + "=" + kv.Value + "&");
				} else {
					builder.Append (kv.Key + "=" + kv.Value);
				}
			}
			return builder.ToString ();
		}
		private IEnumerator _webGet(string url, Dictionary<string,string> info,CallBack_None_Params_String handler){
			UnityWebRequest _get = UnityWebRequest.Get (AppendUrl (url, info));
			yield return _get.Send();

			if (_get.isError) {
				Debug.Log (_get.error);
			} else {
				if (handler != null)
					handler (_get.downloadHandler.text);
			}
		}

//		Web Post
		public void WebPost(string url, Dictionary<string,string> info,CallBack_None_Params_String handler){
			CoroutineBehaviour.StartCoroutine (_webPost (url, info, handler));
		}

		private IEnumerator _webPost(string url, Dictionary<string,string> info,CallBack_None_Params_String handler){
			UnityWebRequest _post = new UnityWebRequest (url,"POST");
			_post.downloadHandler = new DownloadHandlerBuffer ();
			_post.uploadHandler = new UploadHandlerRaw (Encoding.Default.GetBytes (LitJson.JsonMapper.ToJson (info)));
			_post.SetRequestHeader ("Content-Type", "application/json");

			yield return _post.Send ();
			if (_post.isError) {
				Debug.Log (_post.error);
			} else {
				if (handler != null)
					handler (_post.downloadHandler.text);
			}
		}
	}
}
