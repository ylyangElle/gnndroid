package org.arguslab.native_multiple_interactions;
public class MainActivity extends android.app.Activity {

    static MainActivity()
    {
        System.loadLibrary("multiple_interactions");
        return;
    }

    public MainActivity()
    {
        return;
    }

    private void toNative(org.arguslab.native_multiple_interactions.Data p1, String p2)
    {
        p1.str = p2;
        this.propagateImei(p1);
        return;
    }

    public native void leakImei();

    protected void onCreate(android.os.Bundle p2)
    {
        super.onCreate(p2);
        this.setContentView(2131034112);
        if (this.checkSelfPermission("android.permission.READ_PHONE_STATE") != 0) {
            this.requestPermissions(new String[] {"android.permission.READ_PHONE_STATE"}), 1);
        }
        return;
    }

    public void onRequestPermissionsResult(int p1, String[] p2, int[] p3)
    {
        if (p1 == 1) {
            if (this.checkSelfPermission("android.permission.READ_PHONE_STATE") == 0) {
                this.toNative(new org.arguslab.native_multiple_interactions.Data(), ((android.telephony.TelephonyManager) this.getSystemService("phone")).getDeviceId());
                return;
            } else {
                return;
            }
        } else {
            return;
        }
    }

    public native void propagateImei();

    public void toNativeAgain(String p1)
    {
        this.leakImei(p1);
        return;
    }
}
