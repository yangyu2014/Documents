using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

#if UNITY_EDITOR
using UnityEditor;
#endif 

public class UIRoundRawImage : MonoBehaviour {
	public float radius = 25f;
	public bool isHideDown = false;
	private Material mat;

	void Awake(){
		Vector2 size = gameObject.GetComponent<RectTransform> ().sizeDelta;
		Vector4 pic_size = new Vector4 (size.x, size.y, (isHideDown ? 1f : 0f), 0);
		mat = gameObject.GetComponent<RawImage> ().material;
		if (mat == null)
			return;
		mat.SetVector ("pic_size", pic_size);
		mat.SetFloat ("radius", radius);
	}

	#if UNITY_EDITOR
	public static T FindResource<T>(string name)where T : Object{
		//寻找资源目录下的T类型的物体
		Object[] objs = Resources.FindObjectsOfTypeAll<T> ();
		if (objs != null && objs.Length > 0) {
			foreach (Object obj in objs) {
				if (obj.name == name)
					return obj as T;
			}
		}
		//寻找AssetBundle中的T类型的物体
		objs = AssetBundle.FindObjectsOfType<T> ();
		if (objs != null && objs.Length > 0) {
			foreach (Object obj in objs) {
				if (obj.name == name)
					return obj as T;
			}
		}
		//没有找到返回默认的T类型
		return default(T);
	}

	public static GameObject CreateCanvas (){
		GameObject root = new GameObject ("Canvas");
		root.AddComponent<RectTransform> ();
		root.layer = LayerMask.NameToLayer("UI");
		root.AddComponent<Canvas> ().renderMode = RenderMode.ScreenSpaceOverlay;
		root.AddComponent<CanvasScaler> ();
		root.AddComponent<GraphicRaycaster> ();
		Undo.RegisterCreatedObjectUndo(root, "Create " + root.name);
		Selection.activeGameObject = root;
		return root;
	}

	public static EventSystem CreateEvevtSystem(){
		EventSystem eventSys = Object.FindObjectOfType<EventSystem> () ;
		if (eventSys == null) {
			GameObject eventSysObj = new GameObject("EvevetSystem");
			eventSys = eventSysObj.AddComponent<EventSystem> ();
			//GameObjectUtility.SetParentAndAlign(eventSysObj, null);
			eventSysObj.AddComponent<StandaloneInputModule> ();
			Undo.RegisterCreatedObjectUndo(eventSysObj, "Create " + eventSysObj.name);
			Selection.activeGameObject = eventSysObj;
		}
		return eventSys;
	}
		
	public static GameObject GetOrCreateCanvasGameObject(){
		GameObject SelectedObj = Selection.activeGameObject;
		Canvas canvas = (SelectedObj == null ? null : SelectedObj.GetComponent<Canvas> ());
		if (canvas != null && canvas.gameObject.activeInHierarchy)
			return canvas.gameObject;

		canvas = Object.FindObjectOfType<Canvas> ();
		if (canvas != null && canvas.gameObject.activeInHierarchy)
			return canvas.gameObject;

		return CreateCanvas ();
	}

	public static void SetParentForCreatedor(GameObject createdor, MenuCommand menuCmd){
		GameObject parent = menuCmd.context as GameObject;
		if (parent == null || parent.GetComponentInParent<Canvas> () == null) {
			parent = GetOrCreateCanvasGameObject ();
		}

		string uniqueName = GameObjectUtility.GetUniqueNameForSibling (parent.transform, createdor.name);
		createdor.name = uniqueName;
		Undo.RegisterCreatedObjectUndo(createdor, "Create " + createdor.name);
		Undo.SetTransformParent(createdor.transform, parent.transform, "Parent " + createdor.name);
		GameObjectUtility.SetParentAndAlign (createdor, parent);	

//		if(parent != menuCmd.context as GameObject)
			
		CreateEvevtSystem ();

		Selection.activeGameObject = createdor;
	}
		
	[MenuItem("GameObject/UI/RoundRawImage")]
	static void CreateRoundRawImage(MenuCommand menuCmd){
		Vector2 size = new Vector2 (100, 100);
		GameObject root = new GameObject ("New RoundRawImage");
		root.layer = LayerMask.NameToLayer("UI");
		RectTransform rectTransform = root.AddComponent<RectTransform> ();
		rectTransform.sizeDelta = size;

		root.AddComponent<CanvasRenderer> ();

		RawImage image = root.AddComponent<RawImage> ();
		image.raycastTarget = true;
		image.color = Color.white;
		image.texture = null;
		image.material = FindResource<Material> ("Round");

		image.uvRect = new Rect (Vector2.zero, Vector2.one);

		root.AddComponent<UIRoundRawImage> ();

		SetParentForCreatedor (root, menuCmd);
	}
	#endif
}
