.class public Lorg/arguslab/native_multiple_interactions/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"


# direct methods
.method static constructor <clinit>()V
    .locals 1

    const-string v0, "multiple_interactions"

    .line 23
    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 20
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    return-void
.end method

.method private toNative(Lorg/arguslab/native_multiple_interactions/Data;Ljava/lang/String;)V
    .locals 0

    .line 40
    iput-object p2, p1, Lorg/arguslab/native_multiple_interactions/Data;->str:Ljava/lang/String;

    .line 41
    invoke-virtual {p0, p1}, Lorg/arguslab/native_multiple_interactions/MainActivity;->propagateImei(Lorg/arguslab/native_multiple_interactions/Data;)V

    return-void
.end method


# virtual methods
.method public native leakImei(Ljava/lang/String;)V
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 1

    .line 32
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    const/high16 p1, 0x7f050000

    .line 33
    invoke-virtual {p0, p1}, Lorg/arguslab/native_multiple_interactions/MainActivity;->setContentView(I)V

    const-string p1, "android.permission.READ_PHONE_STATE"

    .line 34
    invoke-virtual {p0, p1}, Lorg/arguslab/native_multiple_interactions/MainActivity;->checkSelfPermission(Ljava/lang/String;)I

    move-result p1

    if-eqz p1, :cond_0

    const-string p1, "android.permission.READ_PHONE_STATE"

    .line 35
    filled-new-array {p1}, [Ljava/lang/String;

    move-result-object p1

    const/4 v0, 0x1

    invoke-virtual {p0, p1, v0}, Lorg/arguslab/native_multiple_interactions/MainActivity;->requestPermissions([Ljava/lang/String;I)V

    :cond_0
    return-void
.end method

.method public onRequestPermissionsResult(I[Ljava/lang/String;[I)V
    .locals 0

    const/4 p2, 0x1

    if-eq p1, p2, :cond_0

    return-void

    :cond_0
    const-string p1, "phone"

    .line 53
    invoke-virtual {p0, p1}, Lorg/arguslab/native_multiple_interactions/MainActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Landroid/telephony/TelephonyManager;

    const-string p2, "android.permission.READ_PHONE_STATE"

    .line 54
    invoke-virtual {p0, p2}, Lorg/arguslab/native_multiple_interactions/MainActivity;->checkSelfPermission(Ljava/lang/String;)I

    move-result p2

    if-eqz p2, :cond_1

    return-void

    .line 57
    :cond_1
    invoke-virtual {p1}, Landroid/telephony/TelephonyManager;->getDeviceId()Ljava/lang/String;

    move-result-object p1

    .line 58
    new-instance p2, Lorg/arguslab/native_multiple_interactions/Data;

    invoke-direct {p2}, Lorg/arguslab/native_multiple_interactions/Data;-><init>()V

    .line 59
    invoke-direct {p0, p2, p1}, Lorg/arguslab/native_multiple_interactions/MainActivity;->toNative(Lorg/arguslab/native_multiple_interactions/Data;Ljava/lang/String;)V

    return-void
.end method

.method public native propagateImei(Lorg/arguslab/native_multiple_interactions/Data;)V
.end method

.method public toNativeAgain(Ljava/lang/String;)V
    .locals 0

    .line 45
    invoke-virtual {p0, p1}, Lorg/arguslab/native_multiple_interactions/MainActivity;->leakImei(Ljava/lang/String;)V

    return-void
.end method
