using System;
using System.Collections.Generic;
using System.Reflection;

namespace Lib{
	public class TSingleton<T> {
		static private object _locker = new object();
		static private T _instance;
		static public T Singleton{
			get{ 
				if (_instance == null) {
					lock (_locker) {
						if (_instance == null) {
							//获取无参私有的构造函数或者该类型的引用成员
							ConstructorInfo info = typeof(T).GetConstructor (BindingFlags.NonPublic | BindingFlags.Instance, null, new Type[0], null);
							if (info == null) {
								throw new InvalidOperationException ("Class must contain a private constructor");
							}
							_instance = (T)info.Invoke (null);
						}
					}
				}
				return _instance;
			}
		}
	}
}
