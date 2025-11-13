import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PlaceHolderImages } from "@/lib/placeholder-images";
import { Upload } from "lucide-react";
import Image from "next/image";

export default function SettingsPage() {
  const userAvatar = PlaceHolderImages.find(p => p.id === 'user-avatar-1');

  return (
    <div className="flex flex-col">
        <header className="mb-6">
            <h1 className="text-3xl font-bold font-headline">Settings</h1>
            <p className="text-muted-foreground">Manage your account and application settings.</p>
        </header>

        <Tabs defaultValue="profile" className="flex-1">
            <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="profile">Profile</TabsTrigger>
                <TabsTrigger value="security">Security</TabsTrigger>
                <TabsTrigger value="privacy">Privacy</TabsTrigger>
                <TabsTrigger value="application">App</TabsTrigger>
            </TabsList>

            <TabsContent value="profile" className="mt-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Profile</CardTitle>
                        <CardDescription>This is how others will see you on the site.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="space-y-2">
                            <Label>Avatar</Label>
                            <div className="flex items-center gap-4">
                                {userAvatar && <Image src={userAvatar.imageUrl} alt="User Avatar" width={64} height={64} className="rounded-full" />}
                                <Button variant="outline"><Upload className="w-4 h-4 mr-2" /> Upload</Button>
                            </div>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="username">Username</Label>
                            <Input id="username" defaultValue="john.doe" disabled />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input id="email" type="email" defaultValue="johndoe@example.com" />
                        </div>
                    </CardContent>
                </Card>
            </TabsContent>

            <TabsContent value="security" className="mt-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Security</CardTitle>
                        <CardDescription>Manage your account security settings.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="space-y-4">
                             <Label>Change Password</Label>
                            <div className="grid gap-2">
                                <Input type="password" placeholder="Current Password" />
                                <Input type="password" placeholder="New Password" />
                                <Input type="password" placeholder="Confirm New Password" />
                                <Button className="w-fit">Update Password</Button>
                            </div>
                        </div>
                         <Separator />
                        <div className="flex items-center justify-between rounded-lg border p-4">
                            <div>
                                <h3 className="font-medium">Two-Factor Authentication (2FA)</h3>
                                <p className="text-sm text-muted-foreground">Add an extra layer of security to your account.</p>
                            </div>
                            <Switch />
                        </div>
                    </CardContent>
                </Card>
            </TabsContent>
            
            <TabsContent value="privacy" className="mt-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Privacy</CardTitle>
                        <CardDescription>Control how your data is used and shared.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                         <div className="flex items-center justify-between rounded-lg border p-4">
                            <div>
                                <h3 className="font-medium">Analytics</h3>
                                <p className="text-sm text-muted-foreground">Allow us to collect anonymous analytics data.</p>
                            </div>
                            <Switch defaultChecked/>
                        </div>
                        <Separator/>
                        <div className="space-y-2">
                            <Label>Export Data</Label>
                            <p className="text-sm text-muted-foreground">Download a copy of your data.</p>
                            <Button variant="secondary">Export All Data</Button>
                        </div>
                        <Separator/>
                        <div className="space-y-2">
                            <Label className="text-destructive">Delete Account</Label>
                             <p className="text-sm text-muted-foreground">Permanently delete your account and all associated data. This action is irreversible.</p>
                            <Button variant="destructive">Delete My Account</Button>
                        </div>
                    </CardContent>
                </Card>
            </TabsContent>
            
            <TabsContent value="application" className="mt-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Application Settings</CardTitle>
                        <CardDescription>Customize the look and feel of the app.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="flex items-center justify-between rounded-lg border p-4">
                            <div>
                                <h3 className="font-medium">Dark Mode</h3>
                                <p className="text-sm text-muted-foreground">Toggle between light and dark themes.</p>
                            </div>
                            <Switch />
                        </div>
                        <div className="flex items-center justify-between rounded-lg border p-4">
                            <div>
                                <h3 className="font-medium">Email Notifications</h3>
                                <p className="text-sm text-muted-foreground">Receive updates via email.</p>
                            </div>
                            <Switch defaultChecked/>
                        </div>
                    </CardContent>
                </Card>
            </TabsContent>
        </Tabs>
    </div>
  );
}
