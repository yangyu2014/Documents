// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Lib/Round" {
	Properties{
		_MainTex("Base (RGB)", 2D) = "white" {}
	}
		SubShader{
				Tags { "Queue" = "Transparent" "RenderType" = "Opaque"}
				pass {
					Blend SrcAlpha OneMinusSrcAlpha
					CGPROGRAM
					#pragma vertex vert
					#pragma fragment frag
					#include "unitycg.cginc"
					float4 pic_size;
					float radius;
					sampler2D _MainTex;
					struct v2f {
						float4 pos : SV_POSITION;
						float2 ModeUV: TEXCOORD0;
					};
					v2f vert(appdata_base v) {
						v2f o;
						o.pos = UnityObjectToClipPos(v.vertex);
						o.ModeUV = v.texcoord;
						return o;
					}
					fixed4 frag(v2f i) :COLOR{
						fixed4 col = tex2D(_MainTex,i.ModeUV);
						float2 pos = float2(i.ModeUV.x * pic_size.x ,i.ModeUV.y * pic_size.y);
						float radius2 = radius * radius;
						if (pos.y > pic_size.y - radius) {
							float2 leftUp = float2(radius,pic_size.y - radius);
							float2 rightUp = float2(pic_size.x - radius,pic_size.y - radius);
							if (pos.x < radius) {
								if (((leftUp.x - pos.x) * (leftUp.x - pos.x) + (leftUp.y - pos.y) * (leftUp.y - pos.y)) > (radius2)) {
									col = fixed4(1,1,1,0);
								}
							}
							if (pos.x > pic_size.x - radius) {
								if (((rightUp.x - pos.x) * (rightUp.x - pos.x) + (rightUp.y - pos.y) * (rightUp.y - pos.y)) > (radius2)) {
									col = fixed4(1,1,1,0);
								}
							}
						}

						if (pic_size.z == 1) {
							float2 leftDown = float2(radius,radius);
							float2 rightDown = float2(pic_size.x - radius,radius);
							if (pos.y < radius) {
								if (pos.x < radius) {
									if (((leftDown.x - pos.x) * (leftDown.x - pos.x) + (leftDown.y - pos.y) * (leftDown.y - pos.y)) > (radius2)) {
										col = fixed4(1,1,1,0);
									}
								}
								if (pos.x > pic_size.x - radius) {
									if (((rightDown.x - pos.x) * (rightDown.x - pos.x) + (rightDown.y - pos.y) * (rightDown.y - pos.y)) > (radius2)) {
										col = fixed4(1,1,1,0);
									}
								}
							}
						}

						return col;
						}
						ENDCG
					}

	}
	Fallback "UI/Default"
}
