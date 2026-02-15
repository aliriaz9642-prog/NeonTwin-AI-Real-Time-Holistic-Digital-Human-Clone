using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Newtonsoft.Json;

public class PoseReceiver : MonoBehaviour
{
    [Header("Network Settings")]
    public int port = 5005;
    
    [Header("Full Model Mapping")]
    public Transform[] poseBones;  // 33 Pose landmarks
    public Transform[] leftHandBones; // 21 Hand landmarks
    public Transform[] rightHandBones;
    
    [Header("Smoothing")]
    public float smoothingFactor = 15f;
    
    private UdpClient client;
    private Thread receiveThread;
    private bool isRunning = true;

    [System.Serializable]
    public class HolisticPayload
    {
        public float[][] pose;
        public float[][] left_hand;
        public float[][] right_hand;
        public Metrics metrics;
    }

    [System.Serializable]
    public class Metrics
    {
        public float inference_ms;
        public float fps;
    }

    private HolisticPayload latestPayload;

    void Start()
    {
        client = new UdpClient(port);
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        while (isRunning)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);
                latestPayload = JsonConvert.DeserializeObject<HolisticPayload>(text);
            }
            catch (Exception e)
            {
                Debug.LogWarning("Network buffer sync: " + e.Message);
            }
        }
    }

    void Update()
    {
        if (latestPayload != null)
        {
            if (latestPayload.pose != null) ApplyLandmarks(latestPayload.pose, poseBones);
            if (latestPayload.left_hand != null) ApplyLandmarks(latestPayload.left_hand, leftHandBones);
            if (latestPayload.right_hand != null) ApplyLandmarks(latestPayload.right_hand, rightHandBones);
        }
    }

    void ApplyLandmarks(float[][] landmarks, Transform[] boneArray)
    {
        if (boneArray == null || boneArray.Length == 0) return;

        for (int i = 0; i < boneArray.Length && i < landmarks.Length; i++)
        {
            if (boneArray[i] != null)
            {
                // Mapping MediaPipe Space to Unity World Space
                // X: (val-0.5)*scale, Y: (0.5-val)*scale, Z: -val*scale
                Vector3 targetPos = new Vector3(
                    (landmarks[i][0] - 0.5f) * 2f, 
                    (0.5f - landmarks[i][1]) * 2f, 
                    -landmarks[i][2] * 1.5f // Z-multiplier for depth
                );
                
                boneArray[i].localPosition = Vector3.Lerp(boneArray[i].localPosition, targetPos, Time.deltaTime * smoothingFactor);
            }
        }
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        if (client != null) client.Close();
    }
}
