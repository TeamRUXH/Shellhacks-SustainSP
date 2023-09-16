import './globals.css'
import DashboardLayout from './layouts/dashboard'

export default function Layout({children}) {
  return <DashboardLayout>
    {children}
  </DashboardLayout>
}
