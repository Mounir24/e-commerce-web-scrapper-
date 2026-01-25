from utils.helpers import detect_description_type, process_text_description, process_html_description

desc = """

<div style="background: linear-gradient(135deg, #9f7aea 0%, #b794f6 100%);color: white;padding: clamp(20px, 5vw, 40px);border-radius: 25px;text-align: center;margin-bottom: clamp(20px, 4vw, 40px);position: relative;overflow: hidden">
<div style="position: absolute;top: -50px;right: -50px;width: 100px;height: 100px;border-radius: 50%;opacity: 0.6"></div>
<div style="position: absolute;bottom: -30px;left: -30px;width: 80px;height: 80px;border-radius: 50%"></div>
<h1 style="margin: 0;font-size: clamp(24px, 5vw, 36px);letter-spacing: 1.5px;font-weight: bold;line-height: 1.2">✨ ACM DUOLYS HYAL SÉRUM ANTI-ÂGE</h1>
<p style="margin: clamp(15px, 3vw, 20px) 0 0 0;font-size: clamp(16px, 3vw, 22px);font-weight: 600;opacity: 0.95;text-transform: uppercase;letter-spacing: 0.5px">Soin Concentré Acide Hyaluronique - 15ML</p>
<div style="padding: clamp(8px, 2vw, 12px);border-radius: 15px;margin-top: clamp(15px, 3vw, 20px)">
<p style="margin: 0;font-size: clamp(14px, 2.5vw, 17px);font-style: italic;font-weight: 500">La révolution anti-âge pour peaux matures 40 ans et plus</p>
</div>
</div>
<h2 style="color: #9f7aea;border-bottom: 4px solid #9f7aea;padding-bottom: 12px;font-size: clamp(20px, 4vw, 28px);margin: clamp(25px, 5vw, 35px) 0 clamp(15px, 3vw, 25px) 0;font-weight: bold;text-transform: uppercase;letter-spacing: 1px">🎯 Innovation Sérum Anti-Âge</h2>
<div style="background: linear-gradient(135deg, #f7fafc 0%, #e9d8fd 100%);padding: clamp(20px, 4vw, 30px);border-radius: 20px;border-left: 8px solid #b794f6;margin: clamp(20px, 4vw, 30px) 0">
<p style="font-size: clamp(16px, 3vw, 20px);line-height: 1.8;margin: 0 0 clamp(15px, 3vw, 25px) 0;color: #2d3748;font-weight: 500">Le <strong style="color: #9f7aea">ACM Duolys Hyal Sérum Anti-Âge 15ml</strong> révolutionne le soin anti-âge avec sa <strong style="color: #9f7aea">formule concentrée à l'acide hyaluronique</strong>. Ce sérum unique lutte contre différents signes du vieillissement et protège des radicaux libres, spécialement conçu pour les peaux matures de 40 ans et plus.</p>
</div>
<h2 style="color: #9f7aea;border-bottom: 4px solid #9f7aea;padding-bottom: 12px;font-size: clamp(20px, 4vw, 28px);margin: clamp(25px, 5vw, 35px) 0 clamp(15px, 3vw, 25px) 0;font-weight: bold;text-transform: uppercase;letter-spacing: 1px">✨ Bénéfices Anti-Âge</h2>
<div style="background: linear-gradient(135deg, #9f7aea 0%, #b794f6 100%);padding: clamp(20px, 4vw, 30px);border-radius: 25px;margin: clamp(20px, 4vw, 30px) 0;position: relative;overflow: hidden;border: 2px solid #805ad5">
<div style="position: absolute;top: -30px;right: -30px;width: 120px;height: 120px;background: linear-gradient(45deg, #d6bcfa, #9f7aea);border-radius: 50%;opacity: 0.2"></div>
<div style="position: absolute;bottom: -40px;left: -40px;width: 100px;height: 100px;background: linear-gradient(45deg, #b794f6, #9f7aea);border-radius: 50%;opacity: 0.2"></div>
<div class="mobile-stack" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));gap: clamp(15px, 3vw, 25px)">
<div style="background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);padding: clamp(15px, 3vw, 25px);border-radius: 20px;border: 2px solid #e53e3e;position: relative;overflow: hidden">
<div style="position: absolute;top: 0;left: 0;width: 100%;height: 4px;background: linear-gradient(90deg, #e53e3e, #f56565)"></div>
<div style="align-items: center;margin-bottom: clamp(15px, 3vw, 20px);flex-direction: column;text-align: center">
<div class="mobile-icon" style="background: #e53e3e;color: white;width: clamp(50px, 8vw, 60px);height: clamp(50px, 8vw, 60px);border-radius: 50%;align-items: center;justify-content: center;margin-bottom: 15px;font-size: clamp(24px, 4vw, 28px)">🔄</div>
<p><strong class="mobile-title" style="color: #2d3748;font-size: clamp(16px, 3vw, 20px);font-weight: bold">Anti-Rides Intensif</strong>
</p></div>
<p class="mobile-text" style="margin: 0;color: #555;line-height: 1.7;font-size: clamp(14px, 2.5vw, 16px);text-align: center">Réduit visiblement les rides et ridules d'expression</p>
</div>
<div style="background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);padding: clamp(15px, 3vw, 25px);border-radius: 20px;border: 2px solid #38a169;position: relative;overflow: hidden">
<div style="position: absolute;top: 0;left: 0;width: 100%;height: 4px;background: linear-gradient(90deg, #38a169, #48bb78)"></div>
<div style="align-items: center;margin-bottom: clamp(15px, 3vw, 20px);flex-direction: column;text-align: center">
<div class="mobile-icon" style="background: #38a169;color: white;width: clamp(50px, 8vw, 60px);height: clamp(50px, 8vw, 60px);border-radius: 50%;align-items: center;justify-content: center;margin-bottom: 15px;font-size: clamp(24px, 4vw, 28px)">💧</div>
<p><strong class="mobile-title" style="color: #2d3748;font-size: clamp(16px, 3vw, 20px);font-weight: bold">Hydratation Intense</strong>
</p></div>
<p class="mobile-text" style="margin: 0;color: #555;line-height: 1.7;font-size: clamp(14px, 2.5vw, 16px);text-align: center">Acide hyaluronique pour hydratation profonde et durable</p>
</div>
<div style="background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);padding: clamp(15px, 3vw, 25px);border-radius: 20px;border: 2px solid #3182ce;position: relative;overflow: hidden">
<div style="position: absolute;top: 0;left: 0;width: 100%;height: 4px;background: linear-gradient(90deg, #3182ce, #4299e1)"></div>
<div style="align-items: center;margin-bottom: clamp(15px, 3vw, 20px);flex-direction: column;text-align: center">
<div class="mobile-icon" style="background: #3182ce;color: white;width: clamp(50px, 8vw, 60px);height: clamp(50px, 8vw, 60px);border-radius: 50%;align-items: center;justify-content: center;margin-bottom: 15px;font-size: clamp(24px, 4vw, 28px)">🛡️</div>
<p><strong class="mobile-title" style="color: #2d3748;font-size: clamp(16px, 3vw, 20px);font-weight: bold">Protection Antioxydante</strong>
</p></div>
<p class="mobile-text" style="margin: 0;color: #555;line-height: 1.7;font-size: clamp(14px, 2.5vw, 16px);text-align: center">Lutte contre les radicaux libres et le stress oxydatif</p>
</div>
<div style="background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);padding: clamp(15px, 3vw, 25px);border-radius: 20px;border: 2px solid #d69e2e;position: relative;overflow: hidden">
<div style="position: absolute;top: 0;left: 0;width: 100%;height: 4px;background: linear-gradient(90deg, #d69e2e, #ecc94b)"></div>
<div style="align-items: center;margin-bottom: clamp(15px, 3vw, 20px);flex-direction: column;text-align: center">
<div class="mobile-icon" style="background: #d69e2e;color: white;width: clamp(50px, 8vw, 60px);height: clamp(50px, 8vw, 60px);border-radius: 50%;align-items: center;justify-content: center;margin-bottom: 15px;font-size: clamp(24px, 4vw, 28px)">✨</div>
<p><strong class="mobile-title" style="color: #2d3748;font-size: clamp(16px, 3vw, 20px);font-weight: bold">Éclat Jeunesse</strong>
</p></div>
<p class="mobile-text" style="margin: 0;color: #555;line-height: 1.7;font-size: clamp(14px, 2.5vw, 16px);text-align: center">Redonne luminosité et éclat à la peau mature</p>
</div>
</div>
</div>
<h2 style="color: #9f7aea;border-bottom: 4px solid #9f7aea;padding-bottom: 12px;font-size: clamp(20px, 4vw, 28px);margin: clamp(25px, 5vw, 35px) 0 clamp(15px, 3vw, 25px) 0;font-weight: bold;text-transform: uppercase;letter-spacing: 1px">🧪 Formule Duolys Hyal Avancée</h2>
<div style="background: linear-gradient(135deg, #9f7aea 0%, #b794f6 100%);padding: clamp(20px, 4vw, 25px);border-radius: 20px;margin: clamp(20px, 4vw, 25px) 0;border: 2px solid #805ad5">
<h3 style="color: #ffffff;margin-top: 0;font-size: clamp(18px, 3.5vw, 22px);font-weight: bold;text-align: center;margin-bottom: clamp(20px, 4vw, 25px)">⚗️ COMPLEXE ACTIF ANTI-ÂGE CONCENTRÉ</h3>
<div class="mobile-stack" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));gap: clamp(15px, 3vw, 25px)">
<div class="mobile-padding" style="background: linear-gradient(135deg, #f7fafc 0%, #e9d8fd 100%);padding: clamp(15px, 3vw, 20px);border-radius: 15px">
<h4 style="color: #6b46c1;margin: 0 0 15px 0;font-size: clamp(16px, 3vw, 18px);border-bottom: 2px solid #6b46c1;padding-bottom: 8px">💧 ACIDE HYALURONIQUE</h4>
<ul style="margin: 0;padding-left: 0">
<li style="margin-bottom: 12px;padding-left: 25px;position: relative;font-size: clamp(13px, 2.5vw, 15px)">
<span style="position: absolute;left: 0;color: #e53e3e;font-weight: bold">•</span><strong>Haut Poids Moléculaire</strong> - Hydratation surface</li>
<li style="margin-bottom: 12px;padding-left: 25px;position: relative;font-size: clamp(13px, 2.5vw, 15px)">
<span style="position: absolute;left: 0;color: #e53e3e;font-weight: bold">•</span><strong>Bas Poids Moléculaire</strong> - Pénétration profonde</li>
<li style="margin-bottom: 0;padding-left: 25px;position: relative;font-size: clamp(13px, 2.5vw, 15px)">
<span style="position: absolute;left: 0;color: #e53e3e;font-weight: bold">•</span><strong>Action Repulpante</strong> - Effet lissant immédiat</li>
</ul>
</div>
<div class="mobile-padding" style="background: linear-gradient(135deg, #f7fafc 0%, #e9d8fd 100%);padding: clamp(15px, 3vw, 20px);border-radius: 15px">
<h4 style="color: #6b46c1;margin: 0 0 15px 0;font-size: clamp(16px, 3vw, 18px);border-bottom: 2px solid #6b46c1;padding-bottom: 8px">🛡️ SYSTÈME ANTIOXYDANT</h4>
<ul style="margin: 0;padding-left: 0">
<li style="margin-bottom: 12px;padding-left: 25px;position: relative;font-size: clamp(13px, 2.5vw, 15px)">
<span style="position: absolute;left: 0;color: #38a169;font-weight: bold">•</span><strong>Vitamines C &amp; E</strong> - Protection radicaux libres</li>
<li style="margin-bottom: 12px;padding-left: 25px;position: relative;font-size: clamp(13px, 2.5vw, 15px)">
<span style="position: absolute;left: 0;color: #38a169;font-weight: bold">•</span><strong>Peptides Anti-Âge</strong> - Stimulation cellulaire</li>
<li style="margin-bottom: 0;padding-left: 25px;position: relative;font-size: clamp(13px, 2.5vw, 15px)">
<span style="position: absolute;left: 0;color: #38a169;font-weight: bold">•</span><strong>Texture Sérum</strong> - Absorption rapide optimale</li>
</ul>
</div>
</div>
</div>
<h2 style="color: #9f7aea;border-bottom: 4px solid #9f7aea;padding-bottom: 12px;font-size: clamp(20px, 4vw, 28px);margin: clamp(25px, 5vw, 35px) 0 clamp(15px, 3vw, 25px) 0;font-weight: bold;text-transform: uppercase;letter-spacing: 1px">📋 Protocole d'Application Expert</h2>
<div style="background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);color: white;padding: clamp(20px, 4vw, 25px);border-radius: 20px;margin: clamp(20px, 4vw, 25px) 0">
<h4 style="color: white;margin-bottom: clamp(15px, 3vw, 20px);font-size: clamp(18px, 3.5vw, 20px);text-align: center">🎯 ROUTINE ANTI-ÂGE OPTIMALE</h4>
<div class="mobile-stack" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));gap: clamp(15px, 3vw, 20px)">
<div class="mobile-padding" style="padding: clamp(15px, 3vw, 20px);border-radius: 15px;text-align: center">
<h5 style="color: #d69e2e;margin: 0 0 15px 0;font-size: clamp(16px, 3vw, 18px)">PRÉPARATION</h5>
<p style="margin: 0;font-size: clamp(14px, 2.5vw, 16px);line-height: 1.6"><strong>Peau Propre</strong><br />Nettoyer avec soin adapté</p>
</div>
<div class="mobile-padding" style="padding: clamp(15px, 3vw, 20px);border-radius: 15px;text-align: center">
<h5 style="color: #e53e3e;margin: 0 0 15px 0;font-size: clamp(16px, 3vw, 18px)">APPLICATION</h5>
<p style="margin: 0;font-size: clamp(14px, 2.5vw, 16px);line-height: 1.6"><strong>Quelques Gouttes</strong><br />Masser délicatement visage et cou</p>
</div>
<div class="mobile-padding" style="padding: clamp(15px, 3vw, 20px);border-radius: 15px;text-align: center">
<h5 style="color: #38a169;margin: 0 0 15px 0;font-size: clamp(16px, 3vw, 18px)">TIMING</h5>
<p style="margin: 0;font-size: clamp(14px, 2.5vw, 16px);line-height: 1.6"><strong>Matin et/ou Soir</strong><br />Avant crème hydratante</p>
</div>
<div class="mobile-padding" style="padding: clamp(15px, 3vw, 20px);border-radius: 15px;text-align: center">
<h5 style="color: #3182ce;margin: 0 0 15px 0;font-size: clamp(16px, 3vw, 18px)">CIBLE</h5>
<p style="margin: 0;font-size: clamp(14px, 2.5vw, 16px);line-height: 1.6"><strong>40 ans et plus</strong><br />Peaux matures</p>
</div>
</div>
</div>

<h2 style="color: #9f7aea;border-bottom: 4px solid #9f7aea;padding-bottom: 12px;font-size: clamp(20px, 4vw, 28px);margin: clamp(25px, 5vw, 35px) 0 clamp(15px, 3vw, 25px) 0;font-weight: bold;text-transform: uppercase;letter-spacing: 1px">💰 Offre Exceptionnelle Nova Para</h2>
<div style="background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%);padding: clamp(20px, 4vw, 25px);border-radius: 20px;margin: clamp(20px, 4vw, 25px) 0;border-left: 8px solid #d69e2e">
<div style="text-align: center">
<h3 style="color: #b7791f;margin-top: 0;font-size: clamp(20px, 4vw, 24px);font-weight: bold">🎯 ÉCONOMISEZ 81 MAD</h3>
<div style="justify-content: space-between;align-items: center;margin: clamp(15px, 3vw, 20px) 0;flex-wrap: wrap;gap: 15px">

</div>
</div>
</div>
<div style="background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%);padding: clamp(15px, 3vw, 20px);border-radius: 15px;margin: clamp(20px, 4vw, 25px) 0;text-align: center">
<h3 style="color: #38a169;margin-bottom: clamp(10px, 2vw, 15px);font-size: clamp(18px, 3.5vw, 20px)">🚚 Livraison Premium au Maroc</h3>
<p style="margin: 0;color: #2d3748;font-size: clamp(14px, 2.5vw, 16px);font-weight: 500">Commandez maintenant et recevez votre sérum anti-âge ACM directement chez vous !</p>
</div>
<h2 style="color: #9f7aea;border-bottom: 4px solid #9f7aea;padding-bottom: 12px;font-size: clamp(20px, 4vw, 28px);margin: clamp(25px, 5vw, 35px) 0 clamp(15px, 3vw, 25px) 0;font-weight: bold;text-transform: uppercase;letter-spacing: 1px">🏆 Excellence Dermatologique</h2>
<div style="background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);padding: clamp(20px, 4vw, 25px);border-radius: 15px;border: 2px solid #38b2ac">
<p style="font-size: clamp(16px, 3vw, 18px);line-height: 1.8;margin: 0 0 clamp(15px, 3vw, 20px) 0;color: #2d3748">Sérum anti-âge de référence ACM, développé avec des dermatologues selon les dernières avancées en cosmétologie. Formule Duolys Hyal concentrée spécialement conçue pour peaux matures avec acide hyaluronique haute performance.</p>
<p style="margin: 0;font-style: italic;color: #38b2ac;font-size: clamp(14px, 2.5vw, 16px);font-weight: 600"><strong>Conseil d'expert :</strong> Utilisez régulièrement pour des résultats optimaux. Appliquez avant votre crème habituelle. Convient parfaitement aux peaux de 40 ans et plus en quête de jeunesse.</p>
</div>


 """

results = process_html_description(desc)
print(results)